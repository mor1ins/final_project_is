from Parser import Parser, Fact, Rule
import pprint





if __name__ == '__main__':
    parser = Parser()
    items = parser.parse('facts_and_rules')
    database = {
        'facts': list(filter(lambda item: isinstance(item, Fact), items)),
        'rules': list(filter(lambda item: isinstance(item, Rule), items)),
    }
    database['rules'] = list(map(lambda rule: rule.replace_with_facts(database['facts']), database['rules']))
    pprint.pprint(database)
