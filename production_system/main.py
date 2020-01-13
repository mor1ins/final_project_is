import operator
import re
import string

from Parser import Parser, Fact, Rule
import pprint
from DempsterShafer import calc_dempster_shefer


class ProductionMachine:
    def __init__(self, filename, parser: Parser):
        self._result = []
        _items = parser.parse(filename)
        _database = {
            'facts': list(filter(lambda item: isinstance(item, Fact), _items)),
            'rules': list(filter(lambda item: isinstance(item, Rule), _items)),
        }
        _database['rules'] = list(map(lambda rule: rule.replace_with_facts(_database['facts']), _database['rules']))
        self._database = _database
        self._base = set()
        self._all_facts = set()
        self._all_rules = _database['rules']
        self._finals = self.find_final_facts()

    def set_base(self, base_fact_ids):
        self._base = set(map(lambda fact: self._database['facts'][fact - 1], base_fact_ids))
        self._all_facts = self.base().copy()

    def base(self):
        return self._base

    def facts(self):
        return self._all_facts

    def rules(self):
        return self._all_rules

    def finals(self):
        return self._finals

    def apply(self, rule: Rule):
        print(f'Применяем правило: {rule}')
        fact = rule.right()
        if fact in self.finals():
            self._result.append((fact, rule.weight()))
        self._all_facts.add(rule.right())
        self._all_rules.remove(rule)

    def find_suitable_rules(self):
        return set(filter(lambda rule: len(set(rule.left()) - self.facts()) == 0, self.rules()))

    def find_final_facts(self):
        facts = set(self._database['facts'])
        for rule in self.rules():
            facts -= set(rule.left())
        return facts

    def run(self):
        while True:
            suitable_rules = self.find_suitable_rules()
            for rule in suitable_rules:
                self.apply(rule)
            if len(suitable_rules) == 0:
                return self.facts()

    def result(self):
        return self._result


def get_observation(count, index, value):
    letters = string.ascii_letters[:count]
    elements = list(map(lambda l: f'\'{l[0]}\': {value if l[1] == index else 0.0}', zip(letters, range(len(letters)))))
    elements.append(f'\'{letters}\': {1 - value}')
    return "{ %s }" % ', '.join(elements)


if __name__ == '__main__':
    machine = ProductionMachine('facts_and_rules', Parser())
    # truth = input('Какие факты истины?\r\n')
    truth = '1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 20, 21, 23, 24, 25, 26, 31'
    true_facts = list(map(int, re.split(r",\s*", truth)))
    machine.set_base(true_facts)
    print('База:')
    pprint.pprint(machine.base())
    print()

    print('Вывод:')
    facts = machine.run()
    print('Больше нет правил, которые возможно применить.')
    print()

    results = machine.result()
    facts2 = list(set([result[0] for result in results]))

    observations = []
    for result in results:
        observations.append(get_observation(len(facts2), facts2.index(result[0]), result[1]))
    plses = calc_dempster_shefer(observations)
    for key in plses.keys():
        if len(key) > 1:
            del plses[key]
            break

    maximum = max(plses.items(), key=operator.itemgetter(1))
    maximum = (facts2[string.ascii_lowercase.index(maximum[0])].text(), maximum[1])
    print(maximum)