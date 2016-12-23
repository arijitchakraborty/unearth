from urlparse import  urljoin
from BeautifulSoup import BeautifulSoup


def extract_links(url, response_body):

    links = BeautifulSoup(response_body).findAll('a', href=True)
    if links:
        return [ urljoin(url, e['href']).encode("utf-8") \
        for e in links if e.get('href') \
                            and not e['href'].startswith(u'javascript') \
                            and not e['href'].strip() == u'#' ]
    return []
