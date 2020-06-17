import csv

csv_file_path = r"./csvFile.csv"


def check_csv_file_header():
	with open(csv_file_path, newline='') as csvFile:
		csvFileReader = csv.reader(csvFile, delimiter=',')
		csvFileReader.__next__()
		return csvFileReader.line_num > 0


def get_number_of_fields_in_csv_file():
	with open(csv_file_path, newline='') as csvFile:
		csvFileReader = csv.reader(csvFile, delimiter=',')
		line = csvFileReader.__next__()
	return len(line)


def get_name_of_header_fields():
	with open(csv_file_path, newline='') as csvFile:
		csvFileReader = csv.reader(csvFile, delimiter=',')
		line = csvFileReader.__next__()
	return line


def is_line_contains_empty_cell(line):
	return any('' in s for s in line)


def create_csv_map(header_row, csv_row):
	return dict(zip(header_row,csv_row))


def get_all_lines_in_csv():
	lines=[]
	with open(csv_file_path, newline='') as csvFile:
		csvFileReader = csv.reader(csvFile, delimiter=',')
		# Skip header row
		csvFileReader.__next__()
		for row in csvFileReader:
			lines.append(row)
	return lines

def get_site_prefix(line):
	return line[0]

def get_number_of_turbines_in_csv(line):
	return line[1]
