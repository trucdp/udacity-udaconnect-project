import json
import logging
import os
import psycopg2

from schemas import LocationSchema
from typing import Dict

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-service")


def save_location(location):
    # Verify if a dictionary was provided
    try:
        location_dict = json.loads(location)
    except:
        logger.warning(f"Unexpected non-dictionary payload detected: {location}")
        return

    # Validate the provided location data
    validation_result: Dict = LocationSchema().validate(location_dict)
    if validation_result:
        logger.warning(f"Unexpected data format in payload: {location}, reason: {validation_result}")
        return

    with psycopg2.connect(
        database = DB_NAME,
        user = DB_USERNAME,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    ) as conn:
        person_id = int(location_dict["person_id"])

        with conn.cursor() as cursor:
            try:
                query = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, location_dict["latitude"], location_dict["longitude"])
                cursor.execute(query)
            except Exception as e:
                logger.error(f"Unable to save location data to the database. reason: {e}")