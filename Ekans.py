import shutil
import re
import CsvInteractor,DatabaseInteractor
from DatabaseInteractor import execute_database_query

def create_new_database(csv_map, configuration_db_path):
	site_prefix = CsvInteractor.get_site_prefix(csv_map)
	#site_db = f".\\{site_prefix}-"+configuration_db_path[2:]
	site_db = f".\\Databases\\{site_prefix}-ZubatConfiguration.db"
	copy_database_file(configuration_db_path,site_db)
	print(site_db)
	DatabaseInteractor.configuration_db_path=site_db

def insert_to_turbine_input_table(csv_map):
	table = "TurbineInputTags"
	num_turbines_in_csv = int(CsvInteractor.get_number_of_turbines_in_csv(csv_map))
	cut_off_turbine_num = int(re.search('\d+',CsvInteractor.get_met_backup(csv_map)).group(0))
	num_met_tower = int(CsvInteractor.get_num_met_tower(csv_map))
	list_of_backup_turbines = CsvInteractor.get_turbine_backup(csv_map).split(',')
	print(list_of_backup_turbines)

	#Starts from 2 because T001 is already in the DB
	insert_rows = []
	for i in range (2,num_turbines_in_csv+1):
		met_id = "Met"
		if (i>cut_off_turbine_num) and (num_met_tower >1):
			met_id = "Met2"
		turbine_id = build_turbine_id(i)
		row = get_default_row(table)
		backup_flag = ""
		new_turbine_tuple = generate_new_input_tag_row(list(row[0]), turbine_id, met_id,list_of_backup_turbines)
		insert_rows.append(new_turbine_tuple)
	query = f"INSERT INTO {table} VALUES (?,?,?,?,?,?,?,?,?,?)"
	DatabaseInteractor.execute_many_database_query(query,insert_rows)
	return

def insert_to_turbine_output_table(csv_map):
	table = "TurbineOutputTags"
	num_turbines_in_csv = int(CsvInteractor.get_number_of_turbines_in_csv(csv_map))
	#You'll also have to deal wit hthe met tower, but do this later
	#Starts from 2 because T001 is already in the DB
	insert_rows = []
	for i in range (2,num_turbines_in_csv+1):
		turbine_id = build_turbine_id(i)
		row = get_default_row(table)
		new_turbine_tuple = generate_new_output_tag_row(list(row[0]), turbine_id)
		insert_rows.append(new_turbine_tuple)
	query = f"INSERT INTO {table} VALUES (?,?,?,?,?,?,?,?,?,?,?)"
	DatabaseInteractor.execute_many_database_query(query,insert_rows)
	return

def update_met_tower(csv_map):
	num_met_at_site = CsvInteractor.get_num_met_tower(csv_map)
	if num_met_at_site == '1':
		only_one_met_tower_at_site()
		return
	else:
		for i in range(2,int(num_met_at_site)+1):
			met_id = f"Met{i}"
			insert_new_met_tower_row(met_id)
			temp_tag = CsvInteractor.get_met_temp_tag(csv_map)
			wdspd_tag = CsvInteractor.get_met_wdpsd_tag(csv_map)
			update_met_tower_temp_tag(met_id,temp_tag)
			update_met_tower_wdspd_tag(met_id,wdspd_tag)


def update_site_name( site_name):
	query = f"Update SystemInputTags set DefaultValue = \"{site_name}\" where Description=\"SitePrefix\""
	execute_database_query(query)


def update_latitude( lat):
	query = f"Update SystemInputTags set DefaultValue = \"{lat}\" where Description=\"Lat\""
	execute_database_query(query)


def update_longtitude( lon):
	query = f"Update SystemInputTags set DefaultValue = \"{lon}\" where Description=\"Lon\""
	execute_database_query(query)


def update_utc( utc):
	query = f"Update SystemInputTags set DefaultValue = \"{utc}\" where Description=\"UTCOffset\""
	execute_database_query(query)


def update_met_tower_wdspd_tag(met_id,tag):
	table="MetTowerInputTags"
	query = f"Update {table} set WindSpeedValueTag='{tag}' where MetId='{met_id}'"
	DatabaseInteractor.execute_database_query(query)

def update_met_tower_temp_tag(met_id,tag):
	table="MetTowerInputTags"
	query = f"Update {table} set TempValueTag='{tag}' where MetId='{met_id}'"
	DatabaseInteractor.execute_database_query(query)


def only_one_met_tower_at_site(num_met_tower):
	if num_met_tower == '1':
		query = f"Delete MetTowerInputs where MetId==\"Met2\""
		execute_database_query(query)

def insert_new_met_tower_row(met_id):
	table="MetTowerInputTags"
	default_met_row = DatabaseInteractor.read_database_row(f"Select * from {table} Where MetId='Met'")
	new_row = [tuple([item.replace("Met", met_id) for item in default_met_row[0]])]
	print(new_row)
	query = f"Insert into {table} Values (?,?,?,?)"
	DatabaseInteractor.execute_many_database_query(query,new_row)

	table="MetTowerOutputTags"
	default_met_row = DatabaseInteractor.read_database_row(f"Select * from {table} Where MetId='Met'")
	new_row = [tuple([item.replace("Met", met_id) for item in default_met_row[0]])]
	print(new_row)
	query = f"Insert into {table} Values (?,?,?,?,?,?)"
	DatabaseInteractor.execute_many_database_query(query,new_row)

def copy_database_file( src_file_path, dest_file_path):
	shutil.copy2(src_file_path,dest_file_path)


def build_turbine_id(turbine_num):
	return f"T{turbine_num:03}"


def generate_new_input_tag_row(row,id,metbackup,backup_turbine_list):
	new_row = [item.replace("T001",id) for item in row]
	if is_backup_turbine(new_row[0],backup_turbine_list):
		new_row[5] = "true"
	new_row[9] = metbackup
	return tuple(new_row)

def generate_new_output_tag_row(row,id):
	new_row = [item.replace("T001",id) for item in row]
	return tuple(new_row)

def is_backup_turbine(turbine_row,backup_turbine_list):
	return turbine_row in backup_turbine_list

def make_turbine_backup(turbine_Id):
	DatabaseInteractor.execute_database_query(
		f"Update TurbineInputTags set IsBackupTurbine = 'true' where TurbineId = '{turbine_Id}'")

def get_default_row(turbine_table):
	return DatabaseInteractor.read_database_row(f"SELECT * from {turbine_table} WHERE TurbineId=='T001'")


def update_evaluation_time():
	DatabaseInteractor.execute_database_query(
		f"Update SYsteminputTags set defaultvalue = '10' where description = 'EvaluationPeriod'")
