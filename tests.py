import os, time, unittest

from utils import extract_links
from main import ProducerThread, ConsumerThread


class TestUtilMethods(unittest.TestCase):

    def test_extract_links(self):
        url = 'http://example.com/home'
        html = '''<!DOCTYPE html>
                <html>
                <body>
                    <div id="div1">
                        <a href="/contact-us">This is the 1st link</a>
                    </div>
                    <div id="div2">
                        <a href="http://www.facebook.com">This is the 2nd link</a>
                    </div>
                    <div id="div3">
                        <a href="http://www.twitter.com">This is the 3rd link</a>
                    </div>
                    <div id="div4">
                        <a href="/methods/browse.html">This is the 4th link</a>
                    </div>
                </body>
                </html>'''

        links = extract_links(url, html)

        self.assertTrue(len(links) == 4)
        self.assertTrue(links[0] == 'http://example.com/contact-us')
        self.assertTrue(links[2] == 'http://www.twitter.com')


class TestMainProducerConsumerMethods(unittest.TestCase):

    def test_producer_consumer(self):
        pt = ProducerThread('unittest_input')
        ct = ConsumerThread('unittest_output')
        threads = [pt, ct]

        pt.start()
        ct.start()

        all_done = False
        while not all_done:
            all_done = True
            for t in threads:
                if t.is_alive():
                    all_done = False
                    time.sleep(1)

        f = open('data/unittest_output')

        lines = 0
        for e in f:
            lines += 1
            self.assertTrue(e.strip() == 'http://icanhazip.com/')

        f.close()

        self.assertTrue(lines == 1)
        os.remove('data/unittest_output')


if __name__ == '__main__':
    unittest.main()