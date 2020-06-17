import csv
import sqlite3
import os
import shutil

from pathlib import Path

configuration_db_path=".\ZubatConfiguration.db"

def check_csv_file_header():
	csv_file_path = r"./csvFile.csv"
	with open(csv_file_path, newline='') as csvFile:
		csvFileReader = csv.reader(csvFile, delimiter=',')
		csvFileReader.__next__()
		return csvFileReader.line_num > 0


def get_number_of_fields_in_csv_file():
	csv_file_path = r"./csvFile.csv"
	with open(csv_file_path, newline='') as csvFile:
		csvFileReader = csv.reader(csvFile, delimiter=',')
		line = csvFileReader.__next__()
	return len(line)

def get_name_of_header_fields():
	csv_file_path = r"./csvFile.csv"
	with open(csv_file_path, newline='') as csvFile:
		csvFileReader = csv.reader(csvFile, delimiter=',')
		line = csvFileReader.__next__()
	return line

def is_line_contains_empty_cell(line):
	return any('' in s for s in line)


def configuration_db_exists(configuration_db_path=".\ZubatConfiguration.db"):
	configuration_file = Path(configuration_db_path)
	if configuration_file.is_file():
		return True
	else:
		return False

def connect_to_database(configuration_db_path=".\ZubatConfiguration.db"):
	return sqlite3.connect(configuration_db_path)

def get_number_of_turbines_in_database(configuration_db_path=".\ZubatConfiguration.db"):
	return connect_to_database().cursor().execute("select count(DISTINCT TurbineId) from TurbineOutputTags").fetchone()[0]

def read_database_query(query):
	return connect_to_database().cursor().execute(query).fetchone()[0]

def execute_database_query(query):
	conn = connect_to_database()
	c = conn.cursor()
	c.execute(query)
	conn.commit()
	return

def create_csv_map(header_row, csv_row):
	return dict(zip(header_row,csv_row))

def main():
	return


if __name__ == "main":
	main()


def update_site_name(site_name):
	query = f"Update SystemInputTags set DefaultValue = \"{site_name}\" where Description=\"SitePrefix\""
	execute_database_query(query)

def update_latitude(lat):
	query = f"Update SystemInputTags set DefaultValue = \"{lat}\" where Description=\"Lat\""
	execute_database_query(query)

def update_longtitude(lon):
	query = f"Update SystemInputTags set DefaultValue = \"{lon}\" where Description=\"Lon\""
	execute_database_query(query)

def update_utc(utc):
	query = f"Update SystemInputTags set DefaultValue = \"{utc}\" where Description=\"UTCOffset\""
	execute_database_query(query)

def copy_database_file(src_file_path, dest_file_path):
	shutil.copy2(src_file_path,dest_file_path)
