import CsvInteractor
import Ekans

configuration_db_path=".\ZubatConfiguration.db"


def main():
	header_row = CsvInteractor.get_name_of_header_fields()
	rows = CsvInteractor.get_all_lines_in_csv()
	for row in rows:
		##Verify the row contents first
		if not CsvInteractor.is_line_contains_empty_cell(row):
			csv_map = CsvInteractor.create_csv_map(header_row,row)
			num_turbines = CsvInteractor.get_number_of_turbine()
			#Once verified, create a new site DB
			Ekans.insert_to_database(row)
			##Then update it
			Ekans.update_evaluation_time()
			Ekans.update_latitude()
			Ekans.update_longtitude()
			Ekans.update_site_name()
			Ekans.update_utc()
			Ekans.insert_to_database()
	return

if __name__ == "main":
	main()
