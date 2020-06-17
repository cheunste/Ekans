import shutil

from DatabaseInteractor import execute_database_query
import CsvInteractor, DatabaseInteractor

configuration_db_path=".\ZubatConfiguration.db"


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
