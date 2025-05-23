from datetime import datetime
from typing import Dict, Tuple

import click
from app.db import session_scope
from app.models.scrutin import Ballot, Scrutin, Vote
from app.utils import read_files_from_directory


ParsedData = Tuple[Dict[str, Scrutin], Dict[str, Vote]]

def load_from_json(folder_path:str) -> None:
    """
    Load and parse scrutin JSON files, then insert the parsed data
    into the database.

    Data is read from:
    - SCRUTIN_FOLDER: JSON files defining scutins
    """
    scrutins, votes = parse_scrutin(folder_path)
    click.echo(f"Loading {len(scrutins)} scrutins in database")
    click.echo(f"Loading {len(votes)} votes in database")
    with session_scope() as session:
        session.query(Vote).delete()
        session.query(Scrutin).delete()
        session.add_all(
              list(scrutins.values())
            + list(votes.values())
        )

    """
    Parses JSON files in a folder to extract information about scrutins and their associated votes.

    Args:
        folder_path (str): Path to the folder containing JSON files for scrutins.

    Returns:
        Tuple containing:
            - scrutins (Dict[str, Scrutin])
            - votes (Dict[str, Vote])
    """
def parse_scrutin(folder_path: str) -> ParsedData:
    scrutins = {}
    votes = {}
    for data in read_files_from_directory(folder_path):
        id: str = data["scrutin"]["numero"]
        titre: str = data["scrutin"]["titre"]
        date_scrutin: str = data["scrutin"]["dateScrutin"]
        sort: str = data["scrutin"]["sort"]["code"]
        type: str = data["scrutin"]["typeVote"]["codeTypeVote"]

        scrutin = Scrutin(
            id=id,
            titre=titre,
            date_scrutin=datetime.fromisoformat(date_scrutin),
            sort=sort,
            type=type
        )
        scrutins[id] = scrutin
        for vote in parse_scrutin_votes(data , scrutin):
            votes[f"{vote.scrutin_id}_{vote.depute_id}"] = vote

    return scrutins, votes

def parse_scrutin_votes(
    data: dict,
    scrutin: Scrutin
) -> list[Vote]:
    votes = []
    for groupe in data["scrutin"]["ventilationVotes"]["organe"]["groupes"]["groupe"]:
        votes.extend(process_decompte(groupe["vote"]["decompteNominatif"]["nonVotants"], scrutin, Ballot.NONVOTANT))
        votes.extend(process_decompte(groupe["vote"]["decompteNominatif"]["pours"], scrutin, Ballot.POUR))
        votes.extend(process_decompte(groupe["vote"]["decompteNominatif"]["contres"], scrutin, Ballot.CONTRE))
        votes.extend(process_decompte(groupe["vote"]["decompteNominatif"]["abstentions"], scrutin, Ballot.ABSTENTION))
    return votes


def process_decompte(groupe : dict, scrutin: Scrutin, ballot : Ballot ) -> list[Vote] :
    votes = []
    if groupe:
        groupe = groupe["votant"]
        if isinstance(groupe, list):
            for nv in groupe:
                votes.append(Vote(
                        scrutin_id=scrutin.id,
                        depute_id=nv["acteurRef"],
                        ballot=ballot,
                ))
        else:
            votes.append(Vote(
                scrutin_id=scrutin.id,
                depute_id=groupe["acteurRef"],
                ballot=ballot,
            ))
    return votes
