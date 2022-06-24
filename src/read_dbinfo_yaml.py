import logging
import yaml


def read_dbinfo_yaml(db_yaml):
    """Read database information from yaml file

    Args:
        db_yaml (str): yaml file name with database info

    Returns:
        dict: database information
    """

    logging.info("Reading database information from dbinfo.yaml file")
    try:
        with open("dbinfo.yaml", "r") as f:

            # Read yaml file
            dbinfo = yaml.safe_load(f)

        logging.info("Succesfully loaded dbinfo.yaml")
    except Exception as e:
        logging.exception("Failed to load dbinfo.yaml file")
        return None

    return dbinfo
