import enum
import json
import os
from typing import Dict, Tuple, List

from app import app
from db import session_scope
from models.depute import Depute, GroupParlementaire, Departement, Circonscription, Region

# Type alias for return of parse_deputes
ParsedData = Tuple[Dict[str, Region], Dict[str, Departement], Dict[str, Circonscription], Dict[str, Depute]]


def load_from_json() -> None:
    """
    Load and parse parliamentary group and député JSON files, then insert the parsed data
    into the database using SQLAlchemy.

    Data is read from:
    - ORGANE_FOLDER: JSON files defining parliamentary groups
    - ACTEUR_FOLDER: JSON files defining députés and their mandates
    """
    groupes = parse_organes(app.config["ORGANE_FOLDER"])
    regions, departements, circonscriptions, deputes = parse_deputes(app.config["ACTEUR_FOLDER"], groupes)

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
    for filename in os.listdir(folder_path):
        try:
            with open(os.path.join(folder_path, filename), "r") as file:
                data = json.load(file)
                organe_data = data["organe"]
                organe_id = organe_data["uid"]
                if organe_data["codeType"] == OrganeTypeEnum.GP.value:
                    groupes[organe_id] = GroupParlementaire(
                        id=organe_id,
                        name=organe_data["libelle"]
                    )
        except Exception as e:
            print(f"Error parsing organe file '{filename}': {e}")
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

    for filename in os.listdir(folder_path):
        try:
            with open(os.path.join(folder_path, filename), "r") as file:
                data = json.load(file)
                depute = process_depute_data(data, groupes, regions, departements, circonscriptions)
                deputes[depute.id] = depute
        except Exception as e:
            print(f"Error parsing député file '{filename}': {e}")

    return regions, departements, circonscriptions, deputes


def process_depute_data(
    data: dict,
    groupes: Dict[str, GroupParlementaire],
    regions: Dict[str, Region],
    departements: Dict[str, Departement],
    circonscriptions: Dict[str, Circonscription]
) -> Depute:
    """
    Processes a single député JSON record and returns a Depute instance.

    Args:
        data (dict): Parsed JSON data for a single député.
        groupes (Dict[str, GroupParlementaire]): Mapping of group IDs to group instances.
        regions (Dict[str, Region]): Existing regions to update or reuse.
        departements (Dict[str, Departement]): Existing departments.
        circonscriptions (Dict[str, Circonscription]): Existing constituencies.

    Returns:
        Depute: The constructed Depute instance.
    """
    acteur = data["acteur"]
    depute_id = acteur["uid"]["#text"]
    last_name = acteur["etatCivil"]["ident"]["nom"]
    first_name = acteur["etatCivil"]["ident"]["prenom"]

    mandats = acteur["mandats"]["mandat"]
    organes_ids = find_organe_ids(mandats)
    gp = find_group_parlementaire(organes_ids, groupes)

    circonscription_id, circonscription = find_or_create_circonscription(mandats, regions, departements, circonscriptions)

    return Depute(
        id=depute_id,
        last_name=last_name,
        first_name=first_name,
        gp=gp,
        circonscription=circonscription
    )


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
