import unittest
import os
import csv
import main
from pathlib import Path


class CsvTestClass(unittest.TestCase):
	csv_file_path = r"./csvFile.csv"

	def get_testing_line_from_csv_file(self):
		with open(self.csv_file_path, newline='') as csvFile:
			csvFileReader = csv.reader(csvFile, delimiter=',')
			csvFileReader.__next__()
			line = next(csvFileReader)
		return line

	def test_csv_file_exists(self):
		csv_file_exists = os.path.isfile(self.csv_file_path)
		self.assertTrue(csv_file_exists)

	def test_csv_file_contains_headers(self):
		line = 0
		with open(self.csv_file_path,newline='') as csvFile:
			csvFileReader = csv.reader(csvFile,delimiter=',')
			csvFileReader.__next__()
			line = csvFileReader.line_num
		self.assertTrue(line>0)

	def test_contain_correct_headers(self):
		required_headers = [r"site abbreviation",r"Number of Turbines at Site",r"UTC Offset",r"Turbine Backup",
		                    f"Met Backup Cutoff (inclusive)",r"Latitude",r"Longtitude"]
		with open(self.csv_file_path,newline='') as csvFile:
			csvFileReader = csv.reader(csvFile,delimiter=',')
			line = next(csvFileReader)
		self.assertTrue(line == required_headers,"The CSV file does not contained the required headers")
		self.assertTrue(len(line) == len(required_headers),"The number of items do not match")

	def test_empty_field(self):
		line=self.get_testing_line_from_csv_file()
		self.assertTrue(main.is_line_contains_empty_cell(line))

	def test_create_map(self):
		header_line = main.get_name_of_header_fields()
		dummy_test_list = []
		for i in range (0, len(header_line)):
			dummy_test_list.append(f"Test{i}")
		csv_map = main.create_csv_map(header_line,dummy_test_list)
		self.assertTrue(any(header in csv_map for header in header_line))
		self.assertTrue(any(values in csv_map.values() for values in dummy_test_list))

class DatabaseTestClass(unittest.TestCase):
	csv_file_path = r"./csvFile.csv"
	configuration_db_path = r".\ZubatConfiguration.db"

	def test_configuration_DB_exists(self):
		fileExists = main.configuration_db_exists()
		self.assertTrue(fileExists)

	def test_database_connection(self):
		self.assertIsNotNone(main.connect_to_database())

	def test_read_from_sql(self):
		number_of_turbines = main.get_number_of_turbines_in_database()
		self.assertTrue(number_of_turbines == 19)

	def test_insert_to_db(self):
		query = f"INSERT into TurbineInputTags VALUES ('Test','Test','Test','Test','Test','Test','Test','Test','Test','Test')"
		main.execute_database_query(query)
		number_of_turbines = main.get_number_of_turbines_in_database()
		self.assertTrue(number_of_turbines >= 19)

	def test_remove_from_db(self):
		query = f"Delete from TurbineInputTags WHERE TurbineId=\"Test\""
		main.execute_database_query(query)
		number_of_turbines = main.get_number_of_turbines_in_database()
		self.assertTrue(number_of_turbines == 19)

class EkansTestClass(unittest.TestCase):
	configuration_db_path = r".\ZubatConfiguration.db"
	def test_update_site_name(self):
		site_prefix = "DESER"
		main.update_site_name(site_prefix)
		site_name = main.read_database_query( "select DefaultValue from SystemInputTags where description = \"SitePrefix\"")
		self.assertTrue(site_name == site_prefix)

	def test_update_latitude(self):
		default_lat = 45.59578
		main.update_latitude(default_lat)
		lat = main.read_database_query( "select DefaultValue from SystemInputTags where description = \"Lat\"")
		self.assertTrue(str(lat) == str(default_lat))

	def test_update_longitude(self):
		default_lon = -122.60917
		main.update_longtitude(default_lon)
		lon = main.read_database_query("select DefaultValue from SystemInputTags where description = \"Lon\"")
		self.assertTrue(lon == str(default_lon))

	def test_update_UTC(self):
		default_UTC = -8
		main.update_utc(default_UTC)
		lon = main.read_database_query("select DefaultValue from SystemInputTags where description = \"UTCOffset\"")
		self.assertTrue(lon == str(default_UTC))

	def test_copy_database_file(self):
		file_name = f"Test-ZubatConfiguration.db"
		new_database_file_path = f".\\{file_name}"
		main.copy_database_file(".\ZubatConfiguration.db",new_database_file_path)
		copied_database_exists = os.path.isfile(new_database_file_path)
		self.assertTrue(copied_database_exists)

if __name__ == '__main__':
	unittest.main()
