from urllib.request import urlopen
from urllib import error
import ssl
from link_finder import LinkFinder
import domain
import general


class Spider:
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    broken_file = ''
    queue = set()
    crawled = set()
    broken = set()
    ignore_url = lambda x: False
    max_queue_size = 20000    
    # Needed for sites with expired ssl certificates
    unverified_context = ssl._create_unverified_context()

    def __init__(self, project_name, base_url, domain_name, ignore_url):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.broken_file = Spider.project_name + '/broken.txt'
        
        #ignore_url must be a callable boolean function that tells whether the spider should ignore the inward going link
        Spider.ignore_url = ignore_url
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        general.create_project_dir(Spider.project_name)
        general.create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = general.file_to_set(Spider.queue_file)
        Spider.crawled = general.file_to_set(Spider.crawled_file)
        Spider.broken = general.file_to_set(Spider.broken_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            gathered = Spider.gather_links(page_url)
            if gathered == -1:
                Spider.add_link_to_broken(page_url)
            else:
                Spider.add_links_to_queue(gathered)
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url, context=Spider.unverified_context)
            if Spider.domain_name != domain.get_domain_name(page_url):
                return set()
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except error.HTTPError as e:
            if e.code == 404:
                print(str(e))
                return -1
            else:
                print(str(e))
                return set()
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        if len(Spider.queue) <= Spider.max_queue_size:
            for url in links:
                if (url in Spider.queue) or (url in Spider.crawled):
                    continue
                if (Spider.domain_name == domain.get_domain_name(url)):
                    if (Spider.ignore_url(url)):
                        continue
                Spider.queue.add(url)

    # Saves the found broken links
    @staticmethod
    def add_link_to_broken(url):
        if url in Spider.crawled:
            return
        Spider.broken.add(url)

    @staticmethod
    def update_files():
        general.set_to_file(Spider.queue, Spider.queue_file)
        general.set_to_file(Spider.crawled, Spider.crawled_file)
        general.set_to_file(Spider.broken, Spider.broken_file)
