from flask import Flask, render_template, request

from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search_quotes():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def my_form_post():
    image_urls = []
    quotes=[]
    authors=[]
    length_of_list = 0
    if request.method == "POST":
        search = request.form.get('search')
        to_search = search.replace(" ","-")


        r = requests.get(f"https://www.quotefancy.com/{to_search}-quotes")


        soup = BeautifulSoup(r.content, 'html.parser')
        frame_divs = soup.find_all('img', class_="load-lazily")
        frame_divs2 = soup.find_all('div', class_="frame")

        the_quotes = soup.find_all('p', class_="quote-p")
        the_quotes_authors = soup.find_all('p', class_="author-p")

        for frame_div in frame_divs2:
            a_tags = frame_div.find_all("a")
            for a_tag in a_tags:
                img_tag = a_tag.find("img")
                if img_tag:
                    img_url = img_tag.get("src")  # Use "src" attribute for loaded images
                    if img_url and img_url.startswith("https://"):
                        image_urls.append(img_url)

        for img in frame_divs:
            image_urls.append(img['data-original'])

        for d in the_quotes:
            quotes.append(d.text)
        
        for k in the_quotes_authors:
            if ":" in k.text:
                the_quotes_authors.remove(k)
            

        for a in the_quotes_authors:
            authors.append(a.text)

        length_of_list = len(image_urls)
        indices = range(length_of_list)
          
    return render_template('index.html', image_urls=image_urls, quotes=quotes, authors=authors, length_of_list=length_of_list, indices=indices)
    
quotes = []

@app.route('/show_quotes')
def show_quotes():
    quotes.clear()
    for i in range(4):
        response = requests.get("https://api.quotable.io/random")
        data = response.json()
        quote = f"{data['content']} - {data['author']}"
        quotes.append(quote)

    return render_template('quotes.html', quotes=quotes)


@app.route('/refresh_quotes', methods=['POST'])
def refresh_quotes():
    quotes.clear()
    for i in range(4):
        response = requests.get("https://api.quotable.io/random")
        data = response.json()
        quote = f"{data['content']} - {data['author']}"
        quotes.append(quote)

    return render_template('quotes.html', quotes=quotes)

if __name__ == "__main__":
    app.run(debug=True)