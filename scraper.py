import requests
from lxml import html
import sys
import random

linksToCheck = set([])
linksVisited = []
linksWithErrors = []
correctingLinks = []

logfile = open('scraper.log', 'a')
logfile.write('starting log\n')

def getLinksFromUrl (url):
    linksToCheck.remove(url)
    links = []
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)
        links = tree.xpath('//a/@href')
        linksVisited.append(url)
        logfile.write('link visited [' + url + ']\n')
    except:
        # print('ooops, can''t do it for {' + url + '}, error', sys.exc_info()[0])
        linksWithErrors.append(url)
        print('url error', url)
        logfile.write('error on link [' + url + ']\n')
        return []

    domain = url.replace('https:', '')
    domain = domain.replace('http:', '')
    domain = domain.replace('//', '')
    if domain.startswith('/'):
        domain = domain[1:]
    domain = domain.split('/')[0]

    correctedLinks = []
    for link in links:
        rawLink = link
        if not link.startswith('http'):
            if link.startswith('//'):
                link = 'http:' + link
                # print(1, link, url)
            elif link.startswith('/'):
                base = url.split('/')[1]
                link = 'http://'+ domain + '/' + link
                # print(2, link, base, url)
            else:
                base = url.split('/')[0]
                link = 'http://' + domain + '/' + link
                # print(3, link, base, url)

        correctedLinks.append(link)

        correctingLinks.append((rawLink, link))
        logfile.write('rawlink [' + rawLink + ']; link [' + link + ']; url [' + url + ']; domain [' + domain + ']\n')

    for newLink in correctedLinks:
        linksToCheck.add(newLink)

#    if not 'stackoverflow.com' in url:
#        print('finished, found', len(links), 'links on', url)
    print('[' + url[0:40] +'] to do', len(linksToCheck),'good', len(linksVisited), 'bad', len(linksWithErrors))

    return correctedLinks

firstLink = 'http://stackoverflow.com'
# found = getLinksFromUrl(firstLink)

linksToCheck.add(firstLink)


while len(linksToCheck) > 0:
    link = random.sample(linksToCheck,1)
    getLinksFromUrl(link[0])
