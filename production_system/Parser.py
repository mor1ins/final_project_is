import re


class Item:
    pattern = r""

    def __init__(self, item_id):
        self._id = item_id

    def id(self):
        return self._id

    @staticmethod
    def from_text(text):
        raise Exception('Item is abstract class!')


class Fact(Item):
    pattern = re.compile(r"f(\d+)\s*:\s*(.*)\n")

    def __init__(self, fact_id: int, text: str):
        super().__init__(fact_id)
        self._text = text

    def text(self):
        return self._text

    def __eq__(self, other):
        return self.to_str() == other

    def __hash__(self):
        return hash(self.to_str())

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    def to_str(self):
        return f'Fact({self._id}): "{self._text}"'

    @staticmethod
    def from_text(text):
        groups = Fact.pattern.match(text).groups()
        return Fact(int(groups[0]), groups[1])


class Rule(Item):
    # pattern = re.compile(r"r(\d+)\s*:\s*((f\d+)[\s,]\s*(f\d+)*)\s*->\s*(f\d+),\s*(\d+\.\d+)\n")
    pattern = re.compile(r"r(\d+)\s*:\s*((f\d+)(\s|,\s*f\d+)*)\s*->\s*(f\d+)(,\s*(\d\.\d+))?\n")

    def __init__(self, rule_id: int, left: list, right: str, weight: float):
        super().__init__(rule_id)
        self._left = left
        self._right = right
        self._weight = weight

    def left(self):
        return self._left

    def right(self):
        return self._right

    def weight(self):
        return self._weight

    def __eq__(self, other):
        return self.to_str() == other

    def __hash__(self):
        return hash(self.to_str())

    @staticmethod
    def from_text(text):
        groups = Rule.pattern.match(text).groups()
        premise = re.split(r"[\s,]\s*", groups[1])[:-1]
        conclusion = groups[-3]
        weight = 1.0 if groups[-1] is None else float(groups[-1])
        return Rule(int(groups[0]), premise, conclusion, weight)

    def replace_with_facts(self, facts: list):
        for i in range(len(self._left)):
            fact_id = int(self._left[i][1:])
            for fact in facts:
                if fact.id() == fact_id:
                    self._left[i] = fact
                    break
        fact_id = int(self._right[1:])
        for fact in facts:
            if fact.id() == fact_id:
                self._right = fact

        return self

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    def to_str(self):
        return f'Rule({self._id}): Из {", ".join(map(str, self._left))} следует {self._right}' \
               f' c вероятностью {self._weight * 100:7.3f} %'


class Factory:
    def __init__(self, pattern, make):
        self._pattern = pattern
        self._make = make

    def match(self, text):
        return self._pattern.match(text)

    def valid(self, text):
        return self.match(text) is not None

    def make_from(self, *args, **kwargs):
        return self._make(*args, **kwargs)


class AbstractFactory:
    def __init__(self):
        self._factories = [
            Factory(Fact.pattern, Fact.from_text),
            Factory(Rule.pattern, Rule.from_text)
        ]

    def make_from(self, text):
        for factory in self._factories:
            if factory.valid(text):
                return factory.make_from(text=text)
        raise Exception(f'Incorrect string "{text}"')


class Parser:
    empty_line = re.compile(r'\s*\n')

    def __init__(self):
        self._factory = AbstractFactory()

    def parse(self, filename):
        lines = list(filter(lambda line: self.empty_line.match(line) is None, open(filename, 'r').readlines()))
        return list(map(lambda line: self._factory.make_from(text=line), lines))


if __name__ == "__main__":
    parser = Parser()
    items = parser.parse('facts_and_rules')
    print(items)
