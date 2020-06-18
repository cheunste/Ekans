import CsvInteractor,Ekans

configuration_db_path=".\ZubatConfiguration.db"

def main():
	header_row = CsvInteractor.get_name_of_header_fields()
	rows = CsvInteractor.get_all_lines_in_csv()
	for row in rows:
		##Verify the row contents first
		if not CsvInteractor.is_line_contains_empty_cell(row):
			csv_map = CsvInteractor.create_csv_map(header_row,row)
			num_turbines = CsvInteractor.get_number_of_turbines_in_csv(csv_map)
			print(num_turbines)
			#Once verified, create a new site DB
			Ekans.create_new_database(csv_map, configuration_db_path)
			##Then update it
			Ekans.update_evaluation_time()
			Ekans.update_latitude(CsvInteractor.get_latitude(csv_map))
			Ekans.update_longtitude(CsvInteractor.get_longtitude(csv_map))
			Ekans.update_site_name(CsvInteractor.get_site_prefix(csv_map))
			Ekans.update_utc(CsvInteractor.get_utc_offset(csv_map))
			Ekans.insert_to_turbine_input_table(csv_map)
			Ekans.insert_to_turbine_output_table(csv_map)
			Ekans.update_met_tower(csv_map)
	return

if __name__ == "__main__":
	main()
