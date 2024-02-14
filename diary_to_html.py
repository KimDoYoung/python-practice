# 다음과 같은 프로그램을 만들어 보고 싶어
# 1. mysql 데이터베이스에 접속
# 2. "select * from diary" sql 수행
# 3. sql의 결과를 html 파일로 write
# 참고로 
# 1. diary은 ymd,summary,content 3개의 필드로 되어 있음.
# 2. 모든 필드 즉 3개의 필드는 모두 varchar타입임

import mysql.connector
from mysql.connector import Error
import argparse

# Define format_diary_entry, generate_html_header, and generate_html_footer functions here...

def generate_html_header():
    """Generates the HTML header section with styles."""
    header_html = '''
<html>
<head>
    <style>
        .diary-entry { margin-bottom: 20px; }
        .date { font-weight: bold; }
        .summary, .content { margin: 5px 0; }
    </style>
</head>
<body>
    <h1>Diary Entries</h1>
    '''
    return header_html

def generate_html_footer():
    """Generates the HTML footer section."""
    return '</body></html>'

def format_diary_entry(entry):
    """Formats a diary entry as HTML."""
    entry_html = f"""
    <div class="diary-entry">
        <div class="date">{entry[0]}</div>
        <div class="summary">{entry[1]}</div>
        <div class="content">{entry[2]}</div>
    </div>
    """
    return entry_html

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Generate HTML file from MySQL diary entries.')
    parser.add_argument('output_file', type=str, help='The name of the output HTML file.')
    args = parser.parse_args()
    return args.output_file

def connect_fetch_write(f):
    """Connect to MySQL database, fetch data, and write to an HTML file."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='your_database',
            user='your_username',
            password='your_password'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM diary")
            records = cursor.fetchall()

            f.write(generate_html_header())
            for row in records:
                f.write(format_diary_entry(row))
            f.write(generate_html_footer())
                
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def connect_fetch_write(output_file):
    """Connects to MySQL database, fetches data, and writes to an HTML file specified by the command-line argument."""
    # Existing database connection and data fetching logic goes here...

    with open(output_file, 'w') as f:
        f.write(generate_html_header())
        # Fetching records and writing content logic...
        connect_fetch_write(f) 
        f.write(generate_html_footer())            

if __name__ == '__main__':
    output_file_name = parse_arguments()
    connect_fetch_write(output_file_name)