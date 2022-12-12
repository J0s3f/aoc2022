import math

from lark import Lark, Transformer, v_args

grammar = """
    start: monkey+
    
    monkey: MONKEY id ":" starting_items operation test
    id: INT
    
    MONKEY: "Monkey"
    
    starting_items: "Starting items: " items
    items: INT ("," INT)*
    
    operation: "Operation: new = old" op factor
    factor: INT | old
    old: "old"
    op: multiply | add
    multiply: "*"
    add: "+"
    
    test: "Test: divisible by " INT true_action false_action
    true_action: "If true: throw to monkey " INT
    false_action: "If false: throw to monkey " INT
    
    %import common.INT
    %import common.WS
    %ignore WS
    """


@v_args(inline=True)
class Transformer(Transformer):
    def monkey(self, monkey, id, starting_items, operation, test):
        return Monkey(id, starting_items, operation, test)

    def id(self, id):
        return int(id)

    def starting_items(self, items):
        return [int(x) for x in items.children]

    def operation(self, op, value):
        if hasattr(value.children[0], 'data') and value.children[0].data == "old":
            match op.children[0].data:
                case 'multiply':
                    def f(old):
                        return old * old

                    f.__doc__ = f"old * old"
                    return f
                case 'add':
                    def f(old):
                        return old + old

                    f.__doc__ = f"old + old"
                    return f
        else:
            val = int(value.children[0])
        match op.children[0].data:
            case 'multiply':
                def f(old):
                    return old * val

                f.__doc__ = f"old * {val}"
                return f
            case 'add':
                def f(old):
                    return old + val

                f.__doc__ = f"old + {val}"
                return f
        raise Exception("Error parsing operation")

    def test(self, divisor, true_action, false_action):
        div = int(divisor)
        true_target = int(true_action.children[0])
        false_target = int(false_action.children[0])

        def f(value):
            return true_target if value % div == 0 else false_target

        f.__doc__ = f"""Test: divisible by {div}
    If true: throw to monkey {true_target}
    If false: throw to monkey {false_target}"""
        return f


class Monkey:
    def __init__(self, id, starting_items, operation, test):
        self.id = id
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.monkeys = None
        self.inspected = 0

    def handle_round(self):
        for item in self.items:
            self.inspected += 1
            worry_level = self.operation(item)
            worry_level = worry_level // 3
            target = self.test(worry_level)
            self.monkeys[target].receive(worry_level)
        self.items = []

    def receive(self, item):
        self.items.append(item)

    def __str__(self):
        starting_items_str = ', '.join(map(str, self.items))
        operation_str = self.operation.__doc__
        test_str = self.test.__doc__
        return f"Monkey {self.id}:\n  Starting items: {starting_items_str}\n  Operation: new = {operation_str}\n  {test_str}\n "


parser = Lark(grammar, parser="lalr", transformer=Transformer())

rounds = 20
with open("input", "r") as file:
    monkeys = parser.parse(file.read()).children

for monkey in monkeys:
    monkey.monkeys = monkeys

for _ in range(rounds):
    for monkey in monkeys:
        monkey.handle_round()

monkey_business = math.prod([m.inspected for m in sorted(monkeys, key=lambda x: x.inspected, reverse=True)[:2]])
print("Part 1: " + str(monkey_business))
