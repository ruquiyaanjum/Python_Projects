from flask import Flask, render_template, request
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pymongo
import csv
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route('/')
def index():
    app.logger.info('Rendering index page')
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    app.logger.info(f'Search initiated for keyword: {keyword}')

    try:
        # MongoDB setup
        client = pymongo.MongoClient("mongodb+srv://pwskills:pwskills@cluster0.vwmjzqx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        mydb = client["flipkart_reviews1"]
        mycollection = mydb["reviews"]
        app.logger.info('Connected to MongoDB')

        # Flipkart search URL for the given keyword
        flipkart_url = f"https://www.flipkart.com/search?q={keyword}"
        url_open = urlopen(flipkart_url)
        read_url_open = url_open.read()
        beautify_html_page = bs(read_url_open, "html.parser")
        app.logger.info('Fetched and parsed Flipkart search page')

        # Find all relevant divs
        flipkart_page_many = beautify_html_page.findAll("div", {"class": "cPHDOP col-12-12"})

        # Ensure there are enough divs to process
        if len(flipkart_page_many) < 6:
            app.logger.warning('Not enough product links found')
            raise ValueError("Not enough product links found. Please try a different search keyword.")

        # Remove unwanted divs
        del flipkart_page_many[0:3]
        del flipkart_page_many[-3:]

        # Extract links from the divs
        link = []
        for div in flipkart_page_many:
            for anchor_tag in div.select("a[href]"):
                href_link = anchor_tag["href"]
                link.append(href_link)
        app.logger.info('Extracted product links')

        # Check if there are enough links
        if len(link) < 2:
            app.logger.warning('Not enough product links found after extraction')
            raise ValueError("Not enough product links found. Please try a different search keyword.")

        # Construct the product link
        product_link = f"https://www.flipkart.com{link[1]}"
        app.logger.info(f'Product link constructed: {product_link}')

        # Open the product link and read its content
        url_open1 = urlopen(product_link)
        read_url_open1 = url_open1.read()
        beautify_html_page1 = bs(read_url_open1, "html.parser")
        app.logger.info('Fetched and parsed product details page')

        # Find all relevant divs on the product page
        flipkart_page_many1 = beautify_html_page1.findAll("div", {"class": "col pPAw9M"})

        # Extract the last link from the product page divs
        last_link = None
        for div in flipkart_page_many1:
            for anchor_tag in div.select("a[href]"):
                href_link = anchor_tag["href"]
                last_link = href_link  # Keep updating last_link with the most recent href
        app.logger.info(f'Last link extracted: {last_link}')

        # Construct the full product link
        product_link = f"https://www.flipkart.com{last_link}"
        app.logger.info(f'Full product link constructed: {product_link}')

        # Fetch and parse the product details page
        product_req = urlopen(product_link)
        read_url_open1 = product_req.read()
        product_html = bs(read_url_open1, 'html.parser')
        comment_box = product_html.findAll("div", {"class": "cPHDOP col-12-12"})
        app.logger.info('Fetched and parsed final product details page')

        # Collect results from the comment boxes
        results = []
        for box in comment_box:
            name_element = box.find("p", {"class": "_2NsDsF AwS1CA"})
            ratings_element = box.find("div", {"class": "XQDdHH Ga3i8K"})
            title_element = box.find("p", {"class": "z9E0IG"})
            content_element = box.find("div", {"class": ""})

            if name_element and ratings_element and title_element and content_element:
                result = {
                    "name": name_element.get_text(),
                    "rating": ratings_element.get_text(),
                    "title": title_element.get_text(),
                    "content": content_element.get_text()
                }
                results.append(result)
        app.logger.info('Collected results from comment boxes')

        # Insert results into MongoDB
        mycollection.insert_many(results)
        app.logger.info('Inserted results into MongoDB')

        # Write results to CSV file
        filename = f"{keyword}_reviews.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Ratings", "Title", "Content"])
            for result in results:
                writer.writerow([result['name'], result['rating'], result['title'], result['content']])
        app.logger.info(f'Wrote results to CSV file: {filename}')

        return render_template('result.html', keyword=keyword, reviews=results)

    except Exception as e:
        app.logger.error(f'An error occurred: {e}', exc_info=True)
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
