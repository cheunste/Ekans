import sqlite3
import logging
from pathlib import Path
import DatabaseInteractor

turbine_map_db_path = ".\TurbineNames.db"


def does_table_exist_for_site(site_prefix):

	query = f"SELECT * from {site_prefix}"
	try:
		connect_to_database().cursor().execute(query).fetchone()[1]
		return True
	except:
		return False

def get_frontvue_name_from_table(site_name, turbine_id):
	query = f"SELECT FrontVueName from {site_name} where TurbineId = \"{turbine_id}\""
	try:
		return connect_to_database().cursor().execute(query).fetchone()[0]
	except:
		logging.error(f"Turbine {turbine_id} isn't in the {site_name} table")
		return False



def connect_to_database():
	return sqlite3.connect(turbine_map_db_path)
