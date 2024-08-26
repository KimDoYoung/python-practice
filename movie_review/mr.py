import mariadb
import sys
from jinja2 import Environment, FileSystemLoader
import os

# Database connection details
DB_HOST = 'jskn.iptime.org'
DB_PORT = 3306
DB_USER = 'kdy987'
DB_PASSWORD = 'kalpa987!'
DB_NAME = 'kalpadb'

def fetch_reviews(start_ymd, end_ymd):
    # Connect to the database
    conn = mariadb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
    
    cursor = conn.cursor()
    
    # Query to fetch reviews within the date range
    query = """
    SELECT title, nara, year, lvl, ymd, content 
    FROM movie_review 
    WHERE ymd BETWEEN ? AND ? 
    ORDER BY ymd
    """
    
    cursor.execute(query, (start_ymd, end_ymd))
    
    # Fetch all the results
    reviews = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return reviews

def generate_html(reviews, start_ymd, end_ymd):
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template('template_html.html')
    
    # Generate HTML from template
    html_content = template.render(reviews=reviews)
    
    # Define the output filename
    output_filename = f'movie_review_{start_ymd}_{end_ymd}.html'
    
    # Write the HTML to a file
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print(f'HTML file generated: {output_filename}')

def main():
    if len(sys.argv) != 3:
        print("Usage: review_movie <start_ymd> <end_ymd>")
        sys.exit(1)
    
    start_ymd = sys.argv[1]
    end_ymd = sys.argv[2]
    
    # Fetch movie reviews from the database
    reviews = fetch_reviews(start_ymd, end_ymd)
    
    # Generate HTML file from the reviews
    generate_html(reviews, start_ymd, end_ymd)

if __name__ == "__main__":
    main()
