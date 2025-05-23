import enum
from typing import Dict, Tuple, List

import click

from app.db import session_scope
from app.models.depute import Depute, GroupParlementaire, Departement, Circonscription, Region
from app.utils import read_files_from_directory

# Type alias for return of parse_deputes
ParsedData = Tuple[Dict[str, Region], Dict[str, Departement], Dict[str, Circonscription], Dict[str, Depute]]


def load_from_json( acteurs_folder_path: str, organe_folder_path: str) -> None:
    """
    Load and parse parliamentary group and député JSON files, then insert the parsed data
    into the database using.

    Data is read from:
    - ORGANE_FOLDER: JSON files containing parliamentary group definitions
    - ACTEUR_FOLDER: JSON files containing députés definitions
    """
    groupes = parse_organes(organe_folder_path)
    regions, departements, circonscriptions, deputes = parse_deputes(acteurs_folder_path, groupes)

    click.echo(f"Loading {len(regions)} regions in database")
    click.echo(f"Loading {len(departements)} departements in database")
    click.echo(f"Loading {len(circonscriptions)} circonscriptions in database")
    click.echo(f"Loading {len(deputes)} deputes in database")

    with session_scope() as session:
        session.query(Depute).delete()
        session.query(Circonscription).delete()
        session.query(Departement).delete()
        session.query(Region).delete()
        session.query(GroupParlementaire).delete()
        session.add_all(
              list(groupes.values())
            + list(regions.values())
            + list(departements.values())
            + list(circonscriptions.values())
            + list(deputes.values())
        )



class OrganeTypeEnum(enum.Enum):
    """Enumeration of different types of organes."""
    API = "API"
    ASSEMBLEE = "ASSEMBLEE"
    BUREAU = "BUREAU"
    CIRCONSCRIPTION = "CIRCONSCRIPTION"
    CMP = "CMP"
    CNPS = "CNPS"
    COMNL = "COMNL"
    COMPER = "COMPER"
    COMSENAT = "COMSENAT"
    COMSPSENAT = "COMSPSENAT"
    CONFPT = "CONFPT"
    CONSTITU = "CONSTITU"
    DELEG = "DELEG"
    DELEGBUREAU = "DELEGBUREAU"
    DELEGSENAT = "DELEGSENAT"
    GA = "GA"
    GE = "GE"
    GEVI = "GEVI"
    GOUVERNEMENT = "GOUVERNEMENT"
    GP = "GP"
    GROUPESENAT = "GROUPESENAT"
    MINISTERE = "MINISTERE"
    MISINFO = "MISINFO"
    OFFPAR = "OFFPAR"
    ORGEXTPARL = "ORGEXTPARL"
    PARPOL = "PARPOL"
    PRESREP = "PRESREP"
    SENAT = "SENAT"


def parse_organes(folder_path: str) -> Dict[str, GroupParlementaire]:
    """
    Parse JSON files from the ORGANE_FOLDER to extract parliamentary group data.

    Args:
        folder_path (str): Path to the folder containing JSON files for organes.

    Returns:
        dict: A dictionary mapping organe IDs to GroupParlementaire instances.
    """
    groupes = {}
    for data in read_files_from_directory(folder_path):
        organe_data = data["organe"]
        organe_id = organe_data["uid"]
        if organe_data["codeType"] == OrganeTypeEnum.GP.value:
            groupes[organe_id] = GroupParlementaire(
                id=organe_id,
                name=organe_data["libelle"]
            )
    return groupes


def parse_deputes(folder_path: str, groupes: Dict[str, GroupParlementaire]) -> ParsedData:
    """
    Parses JSON files in a folder to extract information about députés and their associated regions, departments,
    constituencies, and parliamentary groups.

    Args:
        folder_path (str): Path to the folder containing JSON files for députés.
        groupes (Dict[str, GroupParlementaire]): Dictionary mapping group IDs to GroupParlementaire instances.

    Returns:
        Tuple containing:
            - regions (Dict[str, Region])
            - departements (Dict[str, Departement])
            - circonscriptions (Dict[str, Circonscription])
            - deputes (Dict[str, Depute])
    """
    regions = {}
    departements = {}
    circonscriptions = {}
    deputes = {}

    for data in read_files_from_directory(folder_path):
        acteur = data["acteur"]
        depute_id = acteur["uid"]["#text"]
        last_name = acteur["etatCivil"]["ident"]["nom"]
        first_name = acteur["etatCivil"]["ident"]["prenom"]

        mandats = acteur["mandats"]["mandat"]
        organes_ids = find_organe_ids(mandats)
        gp = find_group_parlementaire(organes_ids, groupes)

        circonscription_id, circonscription = find_or_create_circonscription(mandats, regions, departements, circonscriptions)

        deputes[depute_id] = Depute(
            id=depute_id,
            last_name=last_name,
            first_name=first_name,
            gp=gp,
            circonscription=circonscription
        )

    return regions, departements, circonscriptions, deputes


def find_organe_ids(mandats: List[dict]) -> List[str]:
    """
    Finds  all organ reference IDs from a list of mandates.

    Args:
        mandats (list): List of mandate dicts from the JSON data.

    Returns:
        list: A flat list of organ reference IDs.
    """
    organes_ids = []
    for mandat in mandats:
        organes = mandat["organes"]["organeRef"]
        if isinstance(organes, list):
            organes_ids.extend(organes)
        else:
            organes_ids.append(organes)
    return organes_ids


def find_group_parlementaire(organe_ids: List[str], groupes: Dict[str, GroupParlementaire]) -> GroupParlementaire | None:
    """
    Finds the first matching parliamentary group from a list of organ IDs.

    Args:
        organe_ids (list): List of organ reference IDs.
        groupes (Dict[str, GroupParlementaire]): Mapping of group IDs to GroupParlementaire instances.

    Returns:
        GroupParlementaire | None: The first matching group, or None if no match found.
    """
    return next((groupes[oid] for oid in organe_ids if oid in groupes), None)


def find_or_create_circonscription(
    mandats: List[dict],
    regions: Dict[str, Region],
    departements: Dict[str, Departement],
    circonscriptions: Dict[str, Circonscription]
) -> Tuple[str, Circonscription]:
    """
    Finds or creates a Circonscription object (with its associated Département and Region) from a député's mandates.

    Args:
        mandats (list): List of mandate data from the député JSON.
        regions (Dict[str, Region]): Dictionary to store/retrieve Region instances.
        departements (Dict[str, Departement]): Dictionary to store/retrieve Departement instances.
        circonscriptions (Dict[str, Circonscription]): Dictionary to store/retrieve Circonscription instances.

    Returns:
        Tuple[str, Circonscription]: The circonscription ID and corresponding Circonscription instance.

    Raises:
        ValueError: If no valid circonscription is found in the mandates.
    """
    for mandat in mandats:
        election = mandat.get("election")
        if election and election.get("refCirconscription"):
            circonscription_id = election["refCirconscription"]
            dep_code = election["lieu"]["numDepartement"]
            region_name = election["lieu"]["region"]
            dep_name = election["lieu"]["departement"]
            circonscription_code = int(election["lieu"]["numCirco"])

            if region_name not in regions:
                regions[region_name] = Region(name=region_name)

            if dep_code not in departements:
                departements[dep_code] = Departement(
                    code=dep_code,
                    name=dep_name,
                    region=regions[region_name],
                )

            if circonscription_id not in circonscriptions:
                circonscriptions[circonscription_id] = Circonscription(
                    code=circonscription_code,
                    departement=departements[dep_code],
                )

            return circonscription_id, circonscriptions[circonscription_id]

    raise ValueError("No valid circonscription found in mandat data.")
