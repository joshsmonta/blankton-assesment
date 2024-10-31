import sqlite3
import csv

# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

# Open the CSV file
with open('/Users/emmanuel/Downloads/data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row

    # Insert each row into the SQLite table
    for row in csv_reader:
        try:
            cursor.execute('''
                INSERT INTO base_event (room_id, night_of_stay, id, rpg_status, timestamp, hotel_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', row)
        except sqlite3.IntegrityError as e:
            print(f"Skipping row {row[0]}: {e}")


connection.commit()


connection.close()
