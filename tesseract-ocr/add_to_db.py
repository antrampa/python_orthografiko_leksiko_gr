import sqlite3
from datetime import datetime

# Function to create SQLite table if not exists
def create_table():
    conn = sqlite3.connect('../web/words.db')  # Connect to SQLite database or create if not exists
    cursor = conn.cursor()

    # Create Words table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Words (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Word TEXT NOT NULL,
            Extra TEXT,
            Wrong_posibilities TEXT,
            date_create DATETIME NOT NULL,
            date_update DATETIME
        )
    ''')

    conn.commit()
    conn.close()


# Function to read the txt file, parse the lines, and insert into the SQLite database
def process_txt_file(file_path):
    conn = sqlite3.connect('../web/words.db')
    cursor = conn.cursor()

    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into words using ',' as separator
            words = line.strip().split(',')

            # Extract the first word and the rest
            first_word = words[0].strip()
            extra_info = ','.join(words[1:]).strip()

            # Get the current date and time
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insert data into the Words table
            cursor.execute('''
                INSERT INTO Words (word, extra, date_create)
                VALUES (?, ?, ?)
            ''', (first_word, extra_info, current_date))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    #create_table()  # Ensure the table exists before processing the file
    txt_file_path = 'txt/output.txt'  # Change this to the path of your txt file
    process_txt_file(txt_file_path)