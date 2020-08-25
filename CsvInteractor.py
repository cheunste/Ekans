import csv
import re
import TurbineMap

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

def read_turbine_rows_in_file():
	turbine_csv_file_path = ".\\turbinesGepora.csv"
	turbineLines = []
	#Read the turbine rows from the spreadsheet
	with open(turbine_csv_file_path, newline='') as turbineFile:
		csvFileReader = csv.reader(turbineFile, delimiter=',')
		for row in csvFileReader:
			turbineLines.append(row)
	return turbineLines

def create_new_turbine_in_gepora_spreadhsheet(csv_map):
	num_turbines = int(get_number_of_turbines_in_csv(csv_map))
	site_prefix = get_site_prefix(csv_map)
	new_turbine_csv_file_path = f".\\csv\\{site_prefix}-Gepora.csv"
	default_row = read_turbine_rows_in_file()
	turbine_map_exists = False
	frontvue_turbine_name=''

	if TurbineMap.does_table_exist_for_site(site_prefix):
		turbine_map_exists = True

	with open(new_turbine_csv_file_path,'w',newline='\n')as turbineFile:
		csvFileWriter = csv.writer(turbineFile,delimiter=',')
		for i in range (1,num_turbines+1):
			new_turbine_id = f"T{i:03}"
			if turbine_map_exists:
				frontvue_turbine_name = TurbineMap.get_frontvue_name_from_table(site_prefix,new_turbine_id)
			for j in range (0,len(default_row)):
				new_row = [item.replace('T001', new_turbine_id) for item in default_row[j]]
				new_row[27] = frontvue_turbine_name
				csvFileWriter.writerow(new_row)

	return

def is_line_contains_empty_cell(line):
	return any(s=='' in s for s in line)


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
	return line["site prefix"]


def get_number_of_turbines_in_csv(csv_map):
	return csv_map["Number of Turbines at Site"]


def get_utc_offset(csv_map):
	return csv_map['UTC Offset']


def get_turbine_backup(csv_map):
	return csv_map['Turbine Backup']


def get_met_backup(csv_map):
	met_tower_backup = csv_map['Met Backup Cutoff (inclusive)']
	Turbine_num = int(re.search("\d+",met_tower_backup).group())
	print("adfasdfasdf" ,Turbine_num)
	return csv_map['Met Backup Cutoff (inclusive)']


def get_latitude(csv_map):
	return csv_map['Latitude']


def get_longtitude(csv_map):
	return csv_map['Longtitude']


def get_num_met_tower(csv_map):
	return csv_map['Number of Met Towers']


def get_met_wdpsd_tag(csv_map):
	return csv_map["Met WdSpd Tag"]


def get_met_temp_tag(csv_map):
	return csv_map["Met Temp Tag"]
