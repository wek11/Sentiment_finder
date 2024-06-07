from bs4 import BeautifulSoup
import requests, sys, wikipedia, ssl, os
from lxml import html
import re
orig_sslsocket_init = ssl.SSLSocket.__init__
ssl.SSLSocket.__init__ = lambda *args, cert_reqs=ssl.CERT_NONE, **kwargs: orig_sslsocket_init(*args, cert_reqs=ssl.CERT_NONE, **kwargs)

# Filters certain tags out of the text so sentiment analysis is more accurate
def filter_tags(text):
    filtered_text = list = []
    unwanted_tags = set = {"none;", "\"locator", "{\"", "\"type\\"}
    indiv_tag: str = ""

    # Doesn't append tags containing data in the unwanted_tags set #
    # and also stops appending tags past the copyright (near the end of the article) #
    for b in text:
        if "Copyright current_year BBC" in b:
            break
        elif not any(unwanted_tag in b for unwanted_tag in unwanted_tags):
            indiv_tag = b.strip("\"").replace("\\\"", "\"").replace("\\", "\"")

            indiv_tag = indiv_tag.replace("\",\"attributes", "")

            indiv_tag = indiv_tag.replace("\",\"blocks", "")

            indiv_tag = indiv_tag.strip(" ")


            # Doesn't append tag if its not a paragraph
            if len(indiv_tag) > 0:
                if indiv_tag[0].isupper() or indiv_tag[0] == "\"":
                    # Adds the first 15 characters of each tag appended to sorted_text
                    # to unwanted_tags to avoid duplicate text blocks
                    # Adds b instead of indiv_tag b/c data.txt is not filtered
                    unwanted_tags.add(b[:len(b) - 10])

                    filtered_text.append(indiv_tag)

    return filtered_text

# Initial gathering of data and filters out a majority of text
def parse_data(data):
    append_data = boolean = False
    text = list = []
    parsed_data = list = data.split('":')
    for i in parsed_data:
        if append_data:
            text.append(i)
        if "text" in i:
            append_data = True
        else:
            append_data = False

    for i in range(1, len(text)):
        if "www.bbc" in text[-i - 1]:
            text = text[len(text) - i:]
            break

    text = filter_tags(text)

    return text

# Main method to get data, called from views.py
def get_data(url):

    os.environ['CURL_CA_BUNDLE'] = ""
    scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
    scontext.verify_mode = ssl.VerifyMode.CERT_NONE

    # If it's not a wikipedia link, uses my text gathering method. Else, uses wikipedia library
    if ("wikipedia" not in url):
        sys.stdout.reconfigure(encoding='utf-8')
        headers = { 'User-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
                'Accept-Encoding': 'identity'
            }
        params = {
            'action': 'parse',
            'format': 'json',
            'page': url,
            'prop': 'text',
            'redirects':''
        }
        response = requests.get(url, headers=headers)

        return parse_data(response.text)
    else: 
        wikipedia.set_lang(url[8:10])
        page = wikipedia.WikipediaPage(url[30:].replace("_", " ")) 
        return page.content
    
# Strips a string to a list of sentences, called from views,py and analysis.py for ease of use
def strip_to_sentences(text: str, url): 
    
    stripped_list = []
    text_list = '|'.join(text).split("|")

    if "wikipedia" in url:
        print(text)
        return "|".join(re.split(r"=+[a-zA-Z]=+", text))

    for i in range(len(text_list)):
        sentence = text_list[i].replace('"content', "")
        sentence = sentence.replace('"formats', "")
        sentence = sentence.replace('"headline', "")

        sentence = sentence.strip("'\\\",' ")
        sentence = sentence.strip('"[]')
        
        if len(sentence) > 15:
            stripped_list.append(sentence)

    return "|".join(stripped_list)
