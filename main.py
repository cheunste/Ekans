import csv


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

def is_line_contains_empty_fcell(line):
	return any('' in s for s in line)

