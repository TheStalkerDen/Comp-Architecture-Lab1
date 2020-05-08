import os
import unittest

from site_parser import site_parser

dir_path = os.path.dirname(os.path.realpath(__file__))


class GetSiteListFromFileTests(unittest.TestCase):
    def test1(self):
        site_list = site_parser.get_site_list_from_file(dir_path + "/resources/site-list1.xml")
        self.assertEqual(site_list, ["www.site1.org", "www.site2.org"])

    def test2(self):
        site_list = site_parser.get_site_list_from_file(dir_path + "/resources/site-list2.xml")
        self.assertEqual(site_list, ["www.site1.org", "www.site2.org", "www.site3.org"])

    def test3(self):
        site_list = site_parser.get_site_list_from_file(dir_path + "/resources/site-list3.xml")
        self.assertEqual(site_list, [])


class ConvertLinkToAbsoluteTests(unittest.TestCase):
    def test1(self):
        url = site_parser.convert_link_to_absolute("http://www.test.ua/doc/", "22/1.doc")
        self.assertEqual("http://www.test.ua/doc/22/1.doc", url)

    def test2(self):
        url = site_parser.convert_link_to_absolute("http://www.test.ua/doc/", "22/1.html#21")
        self.assertEqual("http://www.test.ua/doc/22/1.html", url)

    def test3(self):
        url = site_parser.convert_link_to_absolute("http://www.test.ua/doc/", "../1.html#21")
        self.assertEqual("http://www.test.ua/1.html", url)


class GetMp3GenreAndTitleTests(unittest.TestCase):
    def test1(self):
        genre, title = site_parser.get_mp3_genre_and_title(dir_path +
                                                           "/resources/All Is Fair In Love And Brostep.mp3")
        self.assertEqual("Dubstep / Breakbeat / Electro House", genre)
        self.assertEqual("All Is Fair In Love And Brostep (Feat. The Ragga Twins)", title)

    def test2(self):
        genre, title = site_parser.get_mp3_genre_and_title(dir_path +
                                                           "/resources/Danheim -Vega.mp3")
        self.assertEqual("Undefined", genre)
        self.assertEqual("No-title", title)


class CollectAllLinksFromHtmlTests(unittest.TestCase):
    def test1(self):
        html_page = '''
        <html>
            <head>
                <title>Test</title>
            </head>
            <body>
                <a href="http://www.testsite.ua/1">TestPage</a>
            </body>
        </html>
        '''
        links = site_parser.collect_all_links_from_html(html_page)
        self.assertEqual(["http://www.testsite.ua/1"], links)

    def test2(self):
        html_page = '''
                <html>
                    <head>
                        <title>Test</title>
                    </head>
                    <body>
                        <a href="http://www.testsite.ua/1">TestPage</a>
                        <div class="test">
                            <a href="doc/2.html">Doc2</a>
                        </div>
                    </body>
                </html>
                '''
        links = site_parser.collect_all_links_from_html(html_page)
        self.assertEqual(["http://www.testsite.ua/1", "doc/2.html"], links)

    def test3(self):
        html_page = '''
                        <html>
                            <head>
                                <title>Test</title>
                            </head>
                            <body>
                            </body>
                        </html>
                        '''
        links = site_parser.collect_all_links_from_html(html_page)
        self.assertEqual([], links)


class GenerateXmlResStringTests(unittest.TestCase):
    def test1(self):
        result = site_parser.generate_xml_res_string({})
        with open(dir_path + "/resources/result1.xml", 'rb') as file:
            expected = file.read()
            self.assertEqual(expected, result)

    def test2(self):
        result = site_parser.generate_xml_res_string({"Genre1": [{"title": "Song", "link": "/1", "filename": "fn"}]})
        with open(dir_path + "/resources/result2.xml", 'rb') as file:
            expected = file.read()
            self.assertEqual(expected, result)


class GenerateXmlResultInResFileTests(unittest.TestCase):
    def test1(self):
        with open(dir_path + "/resources/result.txt", "wb+") as res_file, \
                open(dir_path + "/resources/result1.xml", 'rb') as exp_file:
            site_parser.generate_xml_result_in_result_file({}, res_file)
            res_file.seek(0)
            result = res_file.read()
            expected = exp_file.read()
            self.assertEqual(expected, result)

    def test2(self):
        with open(dir_path + "/resources/result.txt", "wb+") as res_file, \
                open(dir_path + "/resources/result2.xml", 'rb') as exp_file:
            site_parser.generate_xml_result_in_result_file({"Genre1": [{"title": "Song",
                                                                        "link": "/1",
                                                                        "filename": "fn"}]},
                                                           res_file)
            res_file.seek(0)
            result = res_file.read()
            expected = exp_file.read()
            self.assertEqual(expected, result)


class ConvertLinksToAbsoluteTests(unittest.TestCase):
    def test1(self):
        links = site_parser.convert_links_to_absolute("http://www.test.ua/docs/", ["1.html", "../mp3/1.mp3"])
        self.assertEqual(["http://www.test.ua/docs/1.html", "http://www.test.ua/mp3/1.mp3"], links)


class AnalyzeMp3FromLinksTests(unittest.TestCase):
    def test1(self):
        links = ["file:///" + dir_path + "/resources/All Is Fair In Love And Brostep.mp3"]
        result = site_parser.analyze_mp3_from_links(links, use_gevent=False)
        expected = {'Dubstep / Breakbeat / Electro House': [{'filename': 'All Is Fair In Love And '
                                                                         'Brostep.mp3',
                                                             'link': 'file:///' + dir_path + '/resources/All '
                                                                     'Is Fair In Love And '
                                                                     'Brostep.mp3',
                                                             'title': 'All Is Fair In Love And '
                                                                      'Brostep (Feat. The Ragga '
                                                                      'Twins)'}]}
        self.assertEqual(expected, result)

    def test2(self):
        links = ["file:///" + dir_path + "/resources/All Is Fair In Love And Brostep.mp3"]
        result = site_parser.analyze_mp3_from_links(links, use_gevent=True)
        expected = {'Dubstep / Breakbeat / Electro House': [{'filename': 'All Is Fair In Love And '
                                                                         'Brostep.mp3',
                                                             'link': 'file:///' + dir_path + '/resources/All '
                                                                                             'Is Fair In Love And '
                                                                                             'Brostep.mp3',
                                                             'title': 'All Is Fair In Love And '
                                                                      'Brostep (Feat. The Ragga '
                                                                      'Twins)'}]}
        self.assertEqual(expected, result)


class GetMp3LinksTests(unittest.TestCase):
    def test1(self):
        links = ["file:///" + dir_path + "/resources/site.html"]
        result = site_parser.get_mp3_links(links, 2, use_gevent=False)
        self.assertEqual(["file:///" + dir_path + "/resources/All Is Fair In Love And Brostep.mp3",
                          "file:///" + dir_path + "/resources/Danheim -Vega.mp3"], result)

    def test2(self):
        links = ["file:///" + dir_path + "/resources/site.html"]
        result = site_parser.get_mp3_links(links, 2, use_gevent=True)
        self.assertEqual(["file:///" + dir_path + "/resources/All Is Fair In Love And Brostep.mp3",
                          "file:///" + dir_path + "/resources/Danheim -Vega.mp3"], result)


if __name__ == '__main__':
    unittest.main()
