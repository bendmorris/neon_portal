import nose

from dodobase.tools.tax_resolve import get_synonyms, tax_resolve_fuzzy

syn1 = {'Applb': 'Apple', 'Applc': 'Apple', 'Bannnna': 'Banana',
                 'Orangee': 'Orange'}

syn2 = get_synonyms('./dodobase/data/mosquito_synonyms.csv')

def test_apple():
    for l, r in [('appleb', 'Apple'), 
                 ('applb', 'Apple'), 
                 ('apple', 'Apple'), 
                 ('a', 'a'),
                 ('ap', 'ap'), 
                 ('appl', 'Apple'), 
                 ('bionan', 'bionan'), 
                 ('banann', 'Banana'), 
                 ('bannans', 'Banana'),
                 ('bannnna', 'Banana'),
                 ('orangee', 'Orange'),
                 ('Orangee', 'Orange')]:
        yield check_apple, l, r

def check_apple(entered_value, corrected_value):
    new_name = tax_resolve_fuzzy(entered_value, synonyms=syn1)
    new_name = new_name if new_name else entered_value
    assert new_name == corrected_value
    
def test_mosquitos():
    for to_test in ['Aedes clivis', 'Aedes clivid', 'Ochlerotatus clivis', 'Ochlerotatus clivid', 'Ochlarodadus clivus']:
        yield check_mosquitos, to_test

def test_mosquitos_case_sensitivty():
    for to_test in ['Aedes clivis', 'Aedes Clivid', 'ochlerotatus clivis', 'Ochlerotatus Clivid']:
        yield check_mosquitos, to_test
        
def check_mosquitos(sci_name):
    new_name = tax_resolve_fuzzy(sci_name, synonyms=syn2)
    new_name = new_name if new_name else sci_name
    assert new_name == 'Aedes clivis'