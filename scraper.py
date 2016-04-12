import requests
from lxml import html
import sys
import random
import datetime

links_to_check = set([])
links_visited = []
links_with_errors = []

logfile = open('scraper_' + str(datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")) + '.log', 'a')
logfile.write('starting log at ' + str(datetime.datetime.utcnow()) + '\n')


def write_log(message, kind=None):
    string = str(datetime.datetime.utcnow().isoformat())
    string += ' [' + kind + '] '
    string += '`' + message.replace('\n', '\\n') + '`\n'
    logfile.write(string)


def get_links_from_url(url):
    links_to_check.remove(url)
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)
        links = tree.xpath('//a/@href')
        links_visited.append(url)
        write_log('link visited [' + url + '], length (' + str(len(page.content)) + ')', 'log')
    except:
        links_with_errors.append(url)
        print('url error', url)
        write_log('error on link [' + url + '], error [' + str(sys.exc_info()[0]) + ']', 'error')
        return []

    domain = url.replace('https:', '')
    domain = domain.replace('http:', '')
    domain = domain.replace('//', '')
    if domain.startswith('/'):
        domain = domain[1:]
    domain = domain.split('/')[0]

    corrected_links = []
    for single_link in links:
        raw_link = single_link
        new_link = single_link
        if not single_link.startswith('http'):
            if single_link.startswith('//'):
                new_link = 'http:' + single_link
                #print('startswith // making', new_link, 'from', '[' + single_link + ']', 'on', url)
            elif single_link.startswith('/'):
                new_link = 'http://' + domain + single_link
                #print('startswith / making', new_link, 'from domain',
                #      '[' + domain + ']', 'link', '[' + single_link + ']', 'on', url)
            else:
                new_link = 'http://' + domain + '/' + single_link
                #print('startswith - else making', new_link,
                #      'from domain', '[' + domain + ']', 'link', '[' + single_link + ']', 'on', url)

            corrected_links.append(new_link)

            write_log('rawlink [' + raw_link + ']; link [' + single_link
                      + ']; url [' + url + ']; domain [' + domain + ']', 'info')

    for corrected_link in corrected_links:
        if corrected_link not in links_visited:
            links_to_check.add(corrected_link)

#    if not 'stackoverflow.com' in url:
    print('done', len(links_visited) + len(links_with_errors), 'to do', len(links_to_check),
          'good', len(links_visited), 'bad', len(links_with_errors), 'Visited', '[' + url[0:100] + ']', )

    return corrected_links

first_link = 'http://stackoverflow.com'

links_to_check.add(first_link)


while len(links_to_check) > 0:
    link = random.sample(links_to_check, 1)
    get_links_from_url(link[0])
