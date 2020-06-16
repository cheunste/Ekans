import unittest
import os
import csv
import main


class MyTestCase(unittest.TestCase):
	csv_file_path = r"./csvFile.csv"
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
		required_headers = [r"site abbreviation",r"Number of Turbines at Site",r"UTC Offset",r"Turbine Backup",r"Latitude",r"Longtitude"]
		required_headers.sort()
		line =[]
		with open(self.csv_file_path,newline='') as csvFile:
			csvFileReader = csv.reader(csvFile,delimiter=',')
			line = next(csvFileReader)
		line.sort()
		self.assertTrue(line == required_headers,"The CSV file does not contained the required headers")
		self.assertTrue(len(line) == len(required_headers),"The number of items do not match")

	def test_empty_field(self):
		line=self.get_testing_line_from_csv_file()
		line.sort()
		self.assertTrue(main.is_line_contains_empty_fcell(line))

	def test_valid_lat_long(self):
		line = self.get_testing_line_from_csv_file()

	def get_testing_line_from_csv_file(self):
		with open(self.csv_file_path, newline='') as csvFile:
			csvFileReader = csv.reader(csvFile, delimiter=',')
			csvFileReader.__next__()
			line = next(csvFileReader)
		return line

if __name__ == '__main__':
	unittest.main()
