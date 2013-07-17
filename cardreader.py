import requests
from BeautifulSoup import BeautifulSoup


def card_lookup(card="Wrath of God"):
    page = requests.get("http://magiccards.info/query", data={"q": card})
    soup = BeautifulSoup(page.text)
    try:
        content = soup.findAll("table")[3]
    except IndexError:
        return "No matches."
    try:
        actual_title = soup.findAll("span")[0].text
        card_type = " ".join(content.findAll("p")[0].text.replace("\n", "").split())
        card_text = content.findAll("p")[1].text.replace("\n", "")
    except IndexError:
        return "Parsing Error."
    return "[%s] : %s - %s" % (actual_title, card_type, card_text)