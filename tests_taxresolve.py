from dodobase.tools.tax_resolve import get_synonyms, tax_resolve_fuzzy

syn1 = {'applb': 'apple', 'applc': 'apple', 'bannnna': 'banana',
                 'orangee': 'Orange'}

syn2 = get_synonyms('./dodobase/data/mosquito_synonyms.csv')

def test_apple():
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
        yield check_apple, l, r

def check_apple(entered_value, corrected_value):
    new_name = tax_resolve_fuzzy(entered_value, synonyms=syn1)
    new_name = new_name if new_name else entered_value
    assert new_name == corrected_value
    
def test_mosquitos():
    for to_test in ['Aedes clivis', 'Aedes clivid', 'Ochlerotatus clivis', 'Ochlerotatus clivid', 'Ochlarodadus clivus']:
        assert tax_resolve_fuzzy(to_test, synonyms=syn2) == 'Aedes clivis'

def test_mosquitos_case_sensitivty():
    for to_test in ['Aedes clivis', 'Aedes Clivid', 'ochlerotatus clivis', 'Ochlerotatus Clivid']:
        tax_resolve_fuzzy(to_test, synonyms=syn2) == 'Aedes clivis'

if __name__ == '__main__':
    run()
