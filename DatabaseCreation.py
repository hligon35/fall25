import sqlite3
import csv
import os # Import os module to check for file existence and remove if needed

# --- 1. Database Creation  ---
# Define the database file name
DB_FILE = 'books.db'
CSV_FILE = 'books2.csv'

# Remove existing database file to start fresh, if it exists
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Removed existing database file: {DB_FILE}")

# Connect to the SQLite database. If books.db doesn't exist, it will be created.
conn = sqlite3.connect(DB_FILE)
curs = conn.cursor()

# Execute the SQL command to create the 'book' table with specified fields.
# The fields are: title (text), author (text), and year (integer).
curs.execute('''
    CREATE TABLE book (
        title TEXT,
        author TEXT,
        year INTEGER
    )
''')
print(f"Database '{DB_FILE}' and table 'book' created successfully.")

# --- 2. Create the books2.csv file (from Things to Do 16.3) ---
# Data for books2.csv as specified in "things to do 16.3" [3]
books2_csv_content = '''title,author,year
The Weirdstone of Brisingamen,Alan Garner,1960
Perdido Street Station,China Miéville,2000
Thud!,Terry Pratchett,2005
The Spellman Files,Lisa Lutz,2007
Small Gods,Terry Pratchett,1992
'''

# Write the content to books2.csv
with open(CSV_FILE, 'wt', encoding='utf-8') as outfile:
    outfile.write(books2_csv_content)
print(f"Created CSV file: {CSV_FILE}")

# --- 3. Populate the 'book' table from books2.csv (as in Things to Do 16.5) ---
# SQL INSERT statement with placeholders for title, author, and year [2]
ins_str = 'INSERT INTO book (title, author, year) VALUES (?, ?, ?)'

# Open books2.csv and read its data using DictReader [1, 4]
with open(CSV_FILE, 'rt', encoding='utf-8') as infile:
    # DictReader automatically uses the first row as field names [5]
    books = csv.DictReader(infile)
    for book_row in books:
        # Execute the INSERT statement for each row, extracting values by column name [4]
        curs.execute(ins_str, (book_row['title'], book_row['author'], int(book_row['year'])))

# Commit the changes to the database to save the inserted data [2, 4]
conn.commit()
print(f"Data from '{CSV_FILE}' inserted into 'book' table successfully.")

# --- Optional: Verify the data insertion (as in Things to Do 16.6 and 16.7) ---
print("\nVerifying data in 'book' table:")
print("Titles in alphabetical order:")
for (title,) in curs.execute('SELECT title FROM book ORDER BY title ASC'):
    print(f"- {title}")

print("\nAll columns in order of publication (year):")
for title, author, year in curs.execute('SELECT title, author, year FROM book ORDER BY year ASC'):
    print(f"- {year}: {title} — {author}")

# Close the cursor and the database connection
curs.close()
conn.close()
print("\nDatabase connection closed.")