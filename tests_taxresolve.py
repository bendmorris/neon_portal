from unittest import TestCase, main
from dodobase.tools.tax_resolve import get_synonyms, tax_resolve_fuzzy

class TestTaxResolve(TestCase):
    def setUp(self):
        self.syn1 = {'applb': 'apple', 'applc': 'apple', 'bannnna': 'banana',
                     'orangee': 'Orange'}

        self.syn2 = get_synonyms('./dodobase/data/mosquito_synonyms.csv')

    def test_apple(self):
        for l, r in [('appleb', 'apple'), 
                     ('applb', 'apple'), 
                     ('apple', 'apple'), 
                     ('a', 'a'),
                     ('ap', 'ap'), 
                     ('appl', 'apple'), 
                     ('bionan', 'bionan'), 
                     ('banann', 'banana'), 
                     ('bannans', 'banana'),
                     ('bannnna', 'banana'),
                     ('orangee', 'Orange'),
                     ('Orangee', 'Orange')]:
            yield self.check_apple, l, r

    def check_apple(self, entered_value, corrected_value):
        new_name = tax_resolve_fuzzy(entered_value, synonyms=self.syn1)
        new_name = new_name if new_name else entered_value
        self.assertEqual(new_name, corrected_value)
    
    def test_mosquitos(self):
        for to_test in ['Aedes clivis', 'Aedes clivid', 'Ochlerotatus clivis', 'Ochlerotatus clivid', 'Ochlarodadus clivus']:
            self.assertEqual(tax_resolve_fuzzy(to_test, synonyms=self.syn2), 'Aedes clivis')

    def test_mosquitos_case_sensitivty(self):
        for to_test in ['Aedes clivis', 'Aedes Clivid', 'ochlerotatus clivis', 'Ochlerotatus Clivid']:
            self.assertEqual(tax_resolve_fuzzy(to_test, synonyms=self.syn2), 'Aedes clivis')

if __name__ == '__main__':
    main()
