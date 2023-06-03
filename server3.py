from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/search')
def search_images():
    query = request.args.get('query')
    num_images = request.args.get('num_images')

    # build Google Image Search URL
    url = f"https://www.google.com/search?q={query}&tbm=isch"

    # add headers to request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # send request and parse response
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all image elements
    image_elements = soup.find_all('img', limit=int(num_images))

    # extract image URLs and alt text
    results = []
    for image in image_elements:
        if image.has_attr('src') and image.has_attr('alt'):
            image_url = image['src']
            alt_text = image['alt']
            results.append({'image_url': image_url, 'alt_text': alt_text})

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
