# 다음과 같은 프로그램을 만들어 보고 싶어
# 1. mysql 데이터베이스에 접속
# 2. "select * from diary" sql 수행
# 3. sql의 결과를 html 파일로 write
# 참고로 
# 1. diary은 ymd,summary,content 3개의 필드로 되어 있음.
# 2. 모든 필드 즉 3개의 필드는 모두 varchar타입임

import datetime
import html
import os
import re
import mysql.connector
from mysql.connector import Error
import argparse
from dotenv import load_dotenv

load_dotenv()

# Define format_diary_entry, generate_html_header, and generate_html_footer functions here...

def generate_html_header(range):
    """Generates the HTML header section with styles."""
    header_html = '''
<html>
<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>
    <div class='container'>
    <h1>KDY 일지 <span class="text-muted" style="font-size: 1.5rem;">''' + range +'''</span></h1>
    <div>
        <button id="SummaryToggle" class="btn btn-primary">Summary</button>
    </div>'''
    return header_html

def format_date(date_str):
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

def get_weekday_korean(date_str):
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    date_obj = datetime.datetime.strptime(date_str, '%Y%m%d')
    return weekdays[date_obj.weekday()]

def generate_html_footer():
    """Generates the HTML footer section."""
    return '''</div>
    <!-- jQuery CDN - Slim version (without AJAX and effects) -->
    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js"></script>
    <script>
        $(document).ready(function(){
            $("#SummaryToggle").click(function(){
                $('.content').toggle();
            });
            $('.date-summary').click(function() {
                $(this).parent().find('.content').toggle();
            });           
        });
    </script>
    </body></html>'''

def markdown_bold_to_html(s):
    # 정규 표현식을 사용하여 **text**를 <strong>text</strong>으로 변환
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', s)

def str_to_html(s):
    # 문자열 끝의 공백과 줄바꿈 제거
    t = s.rstrip()
    t = html.escape(t)
    t = t.replace("\n", "<br/>")
    trimmed = markdown_bold_to_html(t)
    # 모든 줄바꿈 문자를 <br/>로 바꾸기
    return trimmed

def format_diary_entry(entry,i):
    """Formats a diary entry as HTML."""
    ymd = format_date(entry[0]) 
    dayName = get_weekday_korean(entry[0]) 
    ymdFormat = f"{ymd} ({dayName})"
    content = str_to_html(entry[2])
    className = 'style="color: #000080; background-color: #F5F5DC;"'
    if i % 2 == 1 :
        className = 'style="color: #000000; background-color: #F6F6F5;"'
    entry_html = f"""
    <div class="diary-entry">
        <div class="date-summary  fw-bold" {className}>{ymdFormat} : {entry[1]}</div>
        <div class="content">{content}</div>
    </div>
    """
    return entry_html

def parse_arguments():
    """Parses command-line arguments."""
    current_year = datetime.datetime.now().year
    default_start_date = f"{current_year}0101"
    default_end_date = f"{current_year}1231"
    
    parser = argparse.ArgumentParser(description='Generate HTML file from MySQL diary entries.')
    parser.add_argument('output_file', type=str, help='The name of the output HTML file.')
    parser.add_argument('frYmd', type=str, nargs='?', default=default_start_date, help='The start date in YYYYMMDD format. Optional, defaults to the first day of the current year.')
    parser.add_argument('toYmd', type=str, nargs='?', default=default_end_date, help='The end date in YYYYMMDD format. Optional, defaults to the last day of the current year.')
    args = parser.parse_args()
    return args.output_file, args.frYmd, args.toYmd

def connect_fetch_write(f, frYmd, toYmd):

    """Connect to MySQL database, fetch data, and write to an HTML file."""
    try: 
        connection = mysql.connector.connect(
            host = os.getenv("HOST"),
            database = os.getenv("DATABASE"),
            user = os.getenv("USER"),
            password= os.getenv("PASSWORD"),
            port = os.getenv("PORT")
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"SELECT ymd,summary,content FROM dairy WHERE ymd BETWEEN {frYmd} AND {toYmd}")
            records = cursor.fetchall()
            i=0
            for row in records:
                f.write(format_diary_entry(row,i))
                i=i+1
                
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def run(output_file,frYmd, toYmd):
    """Connects to MySQL database, fetches data, and writes to an HTML file specified by the command-line argument."""
    # Existing database connection and data fetching logic goes here...
    fYmd = format_date(frYmd);
    tYmd = format_date(toYmd);
    r = f"{fYmd} ~ {tYmd}";
    with open(output_file, 'w', encoding='UTF-8') as f:
        f.write(generate_html_header(r))
        # Fetching records and writing content logic...
        connect_fetch_write(f, frYmd, toYmd) 
        f.write(generate_html_footer())            

if __name__ == '__main__':
    output_file_name, frYmd, toYmd = parse_arguments()
    print(f"output file is {output_file_name}")
    try:
        run(output_file_name, frYmd, toYmd)
    except Exception as e:
        print(f"An error occurred: {e}")
