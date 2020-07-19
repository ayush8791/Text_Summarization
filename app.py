from flask import Flask , request , jsonify
import bs4 as bs
import urllib.request
import summaryUtils as utils

app = Flask(__name__)

@app.route('/sample')
def sample():
    scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence') 

    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    paragraphs = parsed_article.find_all('p')

    text = ""

    for p in paragraphs: 
        text += p.text
    return utils.getSummary(text)

@app.route('/summarize', methods = ['GET'])
def summarize():
    content = request.json
    return utils.getSummary(content["text"])

@app.route('/')
def default():
    return '''
    Supported Enpoints are : 
    1. /sample : Sample summarization for Wiki Article on AI
    2. /summarize : takes text return summary
    '''

if __name__ == "__main__":

    app.run(port = 4000)
