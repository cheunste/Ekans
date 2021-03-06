import sqlite3
from pathlib import Path

configuration_db_path=".\ZubatConfiguration.db"

def configuration_db_exists():
	configuration_file = Path(configuration_db_path)
	if configuration_file.is_file():
		return True
	else:
		return False


def connect_to_database():
	return sqlite3.connect(configuration_db_path)


def get_number_of_turbines_in_database(configuration_db_path=".\ZubatConfiguration.db"):
	return connect_to_database().cursor().execute("select count(DISTINCT TurbineId) from TurbineOutputTags").fetchone()[0]


def read_database_query(query):
	return connect_to_database().cursor().execute(query).fetchone()[0]

def read_database_row(query):
	return connect_to_database().cursor().execute(query).fetchall()

def execute_database_query(query):
	conn = connect_to_database()
	c = conn.cursor()
	c.execute(query)
	conn.commit()
	conn.close()
	return

def execute_many_database_query(query, tuple_list):
	conn = connect_to_database()
	c = conn.cursor()
	c.executemany(query,tuple_list)
	conn.commit()
	conn.close()
	return