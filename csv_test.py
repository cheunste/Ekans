import unittest
import os
import csv

import Ekans
import main
import DatabaseInteractor
import CsvInteractor
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
		self.assertTrue(CsvInteractor.is_line_contains_empty_cell(line))

	def test_create_map(self):
		header_line = CsvInteractor.get_name_of_header_fields()
		dummy_test_list = []
		for i in range (0, len(header_line)):
			dummy_test_list.append(f"Test{i}")
		csv_map = CsvInteractor.create_csv_map(header_line,dummy_test_list)
		self.assertTrue(any(header in csv_map for header in header_line))
		self.assertTrue(any(values in csv_map.values() for values in dummy_test_list))

	def test_get_all_liens(self):
		rows = CsvInteractor.get_all_lines_in_csv()
		self.assertTrue(len(rows)>2)

	def test_get_number_of_turbines_in_csv(self):
		expected_prefix = "300"
		test_line = "test, 300, asdfasdf, asdfasdf, -234.0,".split(', ')
		prefix = CsvInteractor.get_number_of_turbines_in_csv(test_line)
		self.assertTrue(prefix == expected_prefix)

	def test_get_site_name_in_csv(self):
		expected_prefix = "test"
		test_line = "test, test, asdfasdf, asdfasdf, -234.0,".split(',')
		prefix = CsvInteractor.get_site_prefix(test_line)
		self.assertTrue(prefix == expected_prefix)

class DatabaseTestClass(unittest.TestCase):
	csv_file_path = r"./csvFile.csv"
	configuration_db_path = r".\ZubatConfiguration.db"

	def test_configuration_DB_exists(self):
		fileExists = DatabaseInteractor.configuration_db_exists()
		self.assertTrue(fileExists)

	def test_database_connection(self):
		self.assertIsNotNone(DatabaseInteractor.connect_to_database())

	def test_read_from_sql(self):
		number_of_turbines = DatabaseInteractor.get_number_of_turbines_in_database()
		self.assertTrue(number_of_turbines == 19)

	def test_insert_to_db(self):

		query = f"INSERT into TurbineInputTags VALUES ('Test','Test','Test','Test','Test','Test','Test','Test','Test','Test')"
		DatabaseInteractor.execute_database_query(query)
		number_of_turbines = DatabaseInteractor.get_number_of_turbines_in_database()
		self.assertTrue(number_of_turbines >= 19)

	def test_remove_from_db(self):
		query = f"Delete from TurbineInputTags WHERE TurbineId=\"Test\""
		DatabaseInteractor.execute_database_query(query)
		number_of_turbines = DatabaseInteractor.get_number_of_turbines_in_database()
		self.assertTrue(number_of_turbines == 19)

	def test_tuple_list_insert(self):
		query = 'INSERT INTO TurbineINputTags VALUES (?,?,?,?,?,?,?,?,?,?)'
		rows = [
		        ('T100','Zubat.T100.Participation','T100.WTUR.TURST.ACTST','T100.WNAC.ExTmp','T100.WNAC.WdSpd','','T100.WTUR.SetTurOp.ActSt.Stop','T100.WTUR.SetTurOp.ActSt.Str','Zubat.T100.PauseTimeOut','Met'),
		        ('T100','Zubat.T100.Participation','T100.WTUR.TURST.ACTST','T100.WNAC.ExTmp','T100.WNAC.WdSpd','','T100.WTUR.SetTurOp.ActSt.Stop','T100.WTUR.SetTurOp.ActSt.Str','Zubat.T100.PauseTimeOut','Met'),
		        ('T100','Zubat.T100.Participation','T100.WTUR.TURST.ACTST','T100.WNAC.ExTmp','T100.WNAC.WdSpd','','T100.WTUR.SetTurOp.ActSt.Stop','T100.WTUR.SetTurOp.ActSt.Str','Zubat.T100.PauseTimeOut','Met')
		        ]
		DatabaseInteractor.execute_many_database_query(query,rows)

		read_query = "SELECT * from TurbineInputTags where TurbineId=='T100'"
		connection = DatabaseInteractor.connect_to_database()
		result = connection.cursor().execute(read_query).fetchall()
		self.assertIsNotNone(result)
		self.assertTrue(len(result) == 3)
		delete_query = "DELETE from TurbineInputTags where TurbineId=='T100'"
		DatabaseInteractor.execute_database_query(delete_query)
		connection.close()

class EkansTestClass(unittest.TestCase):
	configuration_db_path = r".\ZubatConfiguration.db"
	def test_update_site_name(self):
		site_prefix = "DESER"
		Ekans.update_site_name(site_prefix)
		site_name = DatabaseInteractor.read_database_query( "select DefaultValue from SystemInputTags where description = \"SitePrefix\"")
		self.assertTrue(site_name == site_prefix)

	def test_update_latitude(self):
		default_lat = 45.59578
		Ekans.update_latitude(default_lat)
		lat = DatabaseInteractor.read_database_query( "select DefaultValue from SystemInputTags where description = \"Lat\"")
		self.assertTrue(str(lat) == str(default_lat))

	def test_update_longitude(self):
		default_lon = -122.60917
		Ekans.update_longtitude(default_lon)
		lon = DatabaseInteractor.read_database_query("select DefaultValue from SystemInputTags where description = \"Lon\"")
		self.assertTrue(lon == str(default_lon))

	def test_update_UTC(self):
		default_UTC = -8
		Ekans.update_utc(default_UTC)
		lon = DatabaseInteractor.read_database_query("select DefaultValue from SystemInputTags where description = \"UTCOffset\"")
		self.assertTrue(lon == str(default_UTC))

	def test_update_turbine_number(self):
		turbine_num = 5
		new_turbine_id = Ekans.build_turbine_id(turbine_num)
		self.assertTrue(new_turbine_id == "T005")

		turbine_num = 30
		new_turbine_id = Ekans.build_turbine_id(turbine_num)
		self.assertTrue(new_turbine_id == "T030")

		turbine_num = 130
		new_turbine_id = Ekans.build_turbine_id(turbine_num)
		self.assertTrue(new_turbine_id == "T130")

	def test_replace_turbine_number(self):
		dummmy_row = "T001,Zubat.T001.Participation,T001.WTUR.TURST.ACTST," \
		             "T001.WNAC.ExTmp,T001.WNAC.WdSpd,,T001.WTUR.SetTurOp.ActSt.Stop," \
		             "T001.WTUR.SetTurOp.ActSt.Str,Zubat.T001.PauseTimeOut,Met"
		new_id = "T003"
		met_backup = "Met2"
		new_row = Ekans.generate_new_input_tag_row(dummmy_row,new_id,met_backup)
		self.assertFalse(any('T001' in item for item in new_row ))
		self.assertTrue(any(new_id in item for item in new_row ))

	def test_backup_turbine_update(self):
		dummy_row = "T001,Zubat.T001.Participation,T001.WTUR.TURST.ACTST," \
		             "T001.WNAC.ExTmp,T001.WNAC.WdSpd,,T001.WTUR.SetTurOp.ActSt.Stop," \
		             "T001.WTUR.SetTurOp.ActSt.Str,Zubat.T001.PauseTimeOut,Met".split(',')
		backup_turbines = "T001,T003,T049,T099".split(',')
		self.assertTrue(Ekans.is_backup_turbine(dummy_row[0],backup_turbines))
		self.assertFalse(Ekans.is_backup_turbine(dummy_row[0],''))
		if(Ekans.is_backup_turbine(dummy_row[0], backup_turbines)):
			Ekans.make_turbine_backup(dummy_row[0])
		result = DatabaseInteractor.read_database_query(
			f"select isbackupturbine from TurbineInputTags where TurbineId = '{dummy_row[0]}'")
		self.assertTrue(result)
		DatabaseInteractor.execute_database_query(
			f"Update Turbineinputtags set isbackupturbine='' where TurbineId='{dummy_row[0]}'")


	def test_update_evaluation_time(self):
		Ekans.update_evaluation_time()
		result = DatabaseInteractor.read_database_query(
			f"select defaultvalue from systeminputtags where description = 'EvaluationPeriod'")
		print(result)
		self.assertTrue(result == '10')


	def test_copy_database_file(self):
		file_name = f"Test-ZubatConfiguration.db"
		new_database_file_path = f".\\{file_name}"
		Ekans.copy_database_file(".\ZubatConfiguration.db", new_database_file_path)
		copied_database_exists = os.path.isfile(new_database_file_path)
		self.assertTrue(copied_database_exists)


if __name__ == '__main__':
	unittest.main()
