from bs4 import BeautifulSoup
import requests, sys, wikipedia, ssl, os
from lxml import html
orig_sslsocket_init = ssl.SSLSocket.__init__
ssl.SSLSocket.__init__ = lambda *args, cert_reqs=ssl.CERT_NONE, **kwargs: orig_sslsocket_init(*args, cert_reqs=ssl.CERT_NONE, **kwargs)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.
    print('Hello')
    print("hi")


def getHTML(link):
    return requests.get(link)


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
            if indiv_tag[0].isupper() or indiv_tag[0] == "\"":
                # Adds the first 15 characters of each tag appended to sorted_text
                # to unwanted_tags to avoid duplicate text blocks
                # Adds b instead of indiv_tag b/c data.txt is not filtered
                unwanted_tags.add(b[:len(b) - 10])

                filtered_text.append(indiv_tag)

    return filtered_text

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

def get_data(url):
    os.environ['CURL_CA_BUNDLE'] = ""
    scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
    scontext.verify_mode = ssl.VerifyMode.CERT_NONE
    """headers = { 'User-agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
                }
    txt = requests.get(url, headers=headers, verify=False).text
    soup = BeautifulSoup(txt, 'html.parser')
    print(soup.prettify())
    return soup.get_text().split(".")"""
    if ("wikipedia" not in url):
        sys.stdout.reconfigure(encoding='utf-8')
        headers = { 'User-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
            }
        params = {
            'action': 'parse',
            'format': 'json',
            'page': url,
            'prop': 'text',
            'redirects':''
        }
        response = requests.get(url, headers=headers, verify=False)

    #raw_html = response['parse']['text']['*']
    #document = html.document_fromstring(raw_html)

        print(response.text)
        return parse_data(response.text)
    else: 
        print(url[8:10])
        print(url[30:])
        wikipedia.set_lang(url[8:10])
        page = wikipedia.WikipediaPage(url[30:].replace("_", " "))
        print(page.content)
        return page.content
    
def strip_to_sentences(text_list: list): 
    prefixes = {"Mr", "Mrs", "Dr", "Miss"}
    stripped_list = []

    for i in range(len(text_list)):
        sentence = text_list[i].replace('"content', "")
        sentence = sentence.replace('"formats', "")
        sentence = sentence.replace('"headline', "")
        sentence = sentence.strip("'\\\",' ")
        if len(sentence) > 15:
            stripped_list.append(sentence)
        
    return stripped_list
