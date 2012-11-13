from dodobase.tools.get_mendeley_data import get_mendeley_data, citation

class TestMendeleyTags(TestCase):
    def setUp(self):
        self.urls = [
                     "http://www.mendeley.com/research/niche-neutrality/",
                     "http://www.mendeley.com/research/local-interactions-select-lower-pathogen-infectivity/",
                     "http://www.mendeley.com/research/widespread-amphibian-extinctions-epidemic-disease-driven-global-warming/",
                     ]

        self.data_docs = []
        self.citations = []
        for url in self.urls:
            self.data_docs.append(get_mendeley_data(url))
            self.citations.append(citation(url))

        print '\n\n'.join(self.citations)

    def test_mendeley_tags(self):
        for data_doc, citation, (title, year, published_in, in_citation) in zip(self.data_docs, self.citations,
        [
         ('A niche for neutrality', 2007, 'Ecology Letters', 'Adler, P. B.'),
         ('Local interactions select for lower pathogen infectivity', 2007, 'Science', 'Boots, M.'),
         ('Widespread amphibian extinctions from epidemic disease driven by global warming', 2006, 'Nature', 'Pounds, J. A.'),
        ]):
            self.assertEqual(data_doc['title'], title)
            self.assertEqual(data_doc['year'], year)
            self.assertEqual(data_doc['published_in'], published_in)
            self.assertIn(in_citation, citation)

if __name__ == '__main__':
    main()