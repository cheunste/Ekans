import shutil

import CsvInteractor,DatabaseInteractor
from DatabaseInteractor import execute_database_query
from main import configuration_db_path

def insert_to_database( line):
	site_prefix = CsvInteractor.get_site_prefix(line)
	site_db = f".\\{site_prefix}"+configuration_db_path[1:]
	copy_database_file(configuration_db_path,site_db)


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


def copy_database_file( src_file_path, dest_file_path):
	shutil.copy2(src_file_path,dest_file_path)


def build_turbine_id(turbine_num):
	return f"T{turbine_num:03}"


def generate_new_input_tag_row(row,id,metbackup):
	new_row = [item.replace("T001",id) for item in row.split(',')]
	new_row[9] = metbackup
	print(tuple(new_row))
	return tuple(new_row)


def is_backup_turbine(turbine_row,backup_turbine_list):
	return turbine_row in backup_turbine_list

def make_turbine_backup(turbine_Id):
	DatabaseInteractor.execute_database_query(
		f"Update TurbineInputTags set IsBackupTurbine = 'true' where TurbineId = '{turbine_Id}'")


def update_evaluation_time():
	DatabaseInteractor.execute_database_query(
		f"Update SYsteminputTags set defaultvalue = '10' where description = 'EvaluationPeriod'")
