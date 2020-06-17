import CsvInteractor
import Ekans

configuration_db_path=".\ZubatConfiguration.db"


def main():
	rows = CsvInteractor.get_all_lines_in_csv()
	for row in rows:
		#Ekans.insert_to_database(row)
		print(row)
	return

if __name__ == "main":
	main()
