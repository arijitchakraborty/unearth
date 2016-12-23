import sys, time, requests, csv

from Queue import Queue
from threading import Thread
from utils import extract_links


QUEUE_SIZE = 10


# global vars
queue = Queue(QUEUE_SIZE)
production_complete = False


class FetchUrlContentThread(Thread):

    def __init__(self, url):
        self.url = url
        super(self.__class__, self).__init__()

    def run(self):
        global queue
        try:
            r = requests.get(self.url)
            queue.put((self.url, r.text))
        except Exception as e:
            print "EXCEPTION : Unexpected error while fetching response for " + self.url + " :", e


class ProducerThread(Thread):

    def __init__(self, input_file):
        self.input_file = input_file
        super(self.__class__, self).__init__()

    def run(self):
        global queue, production_complete
        threads = []

        if self.input_file:
            try:
                f = open('data/' + self.input_file)
                for url in f:
                    t = FetchUrlContentThread(url.strip())
                    threads.append(t)
                    t.start()
                f.close()

                for t in threads: t.join()
            except Exception as e:
                print "EXCEPTION : Unexpected error while reading input file " + input_file + " :", e


        production_complete = True

        # for shutdown
        queue.put((None, None))


class ConsumerThread(Thread):

    def __init__(self, output_file):
        self.output_file = output_file
        super(self.__class__, self).__init__()

    def run(self):
        global queue, production_complete
        while not queue.empty() or not production_complete:
            url, response_html = queue.get()

            if url is not None and response_html is not None:
                try:
                    links = extract_links(url, response_html)
                    with open('data/' +  self.output_file, 'a') as output:
                        csv.writer(output).writerow([url] + links)
                except Exception as e:
                    print "EXCEPTION : Unexpected error while processing response for " + url + " :", e

            queue.task_done()


if __name__ == '__main__':

    kwargs = dict(x.split('=', 1) for x in sys.argv[1:])
    input_file = kwargs.get('input_file')
    output_file = kwargs.get('output_file')

    ProducerThread(input_file).start()
    ConsumerThread(output_file or (input_file + '_output.csv')).start()
