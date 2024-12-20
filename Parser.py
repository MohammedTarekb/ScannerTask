class TopDownParser:
    def __init__(self):
        self.grammar = {}
        self.terminals = set()
        self.non_terminals = set()
        self.first_sets = {}
        self.follow_sets = {}

    def define_grammar(self):
        print("Define the grammar:")

        # Define Non-terminals and their production rules
        for _ in range(2):
            non_terminal = input("Enter Non-terminal: ").strip()

            self.non_terminals.add(non_terminal)
            self.grammar[non_terminal] = []

            for i in range(2):
                rule = input(f"Enter production rule {i + 1} for '{non_terminal}' separated by space: ").strip()
                self.grammar[non_terminal].append(rule)
                # Update terminals and non-terminals
                for symbol in rule.split():
                    if symbol.islower():
                        self.terminals.add(symbol)
                    else:
                        self.non_terminals.add(symbol)

        print("Grammar defined successfully.")
        print(f"Non-terminals: {self.non_terminals}")
        print(f"Terminals: {self.terminals}")

    def is_simple(self):
        # Check if all production rules start with a terminal
        for non_terminal, rules in self.grammar.items():
            for rule in rules:
                if not rule.split()[0].islower():
                    print(f"Production rule '{non_terminal} -> {rule}' does not start with a terminal.")
                    return False
        return True

    def compute_first_sets(self):
        # Compute the First sets for all non-terminals
        for non_terminal in self.non_terminals:
            self.first_sets[non_terminal] = self._compute_first(non_terminal)

    def _compute_first(self, non_terminal):
        first_set = set()
        for rule in self.grammar.get(non_terminal, []):
            symbols = rule.split()
            if symbols[0] in self.terminals:
                first_set.add(symbols[0])
            else:
                first_set.update(self._compute_first(symbols[0]))
        return first_set

    def compute_follow_sets(self):
        # Compute the Follow sets for all non-terminals
        for non_terminal in self.non_terminals:
            self.follow_sets[non_terminal] = self._compute_follow(non_terminal)

    def _compute_follow(self, non_terminal):
        follow_set = set()
        for lhs, rules in self.grammar.items():
            for rule in rules:
                symbols = rule.split()
                if non_terminal in symbols:
                    index = symbols.index(non_terminal)
                    if index + 1 < len(symbols):
                        next_symbol = symbols[index + 1]
                        if next_symbol in self.terminals:
                            follow_set.add(next_symbol)
                        else:
                            follow_set.update(self.first_sets.get(next_symbol, set()))
                    else:
                        follow_set.update(self.follow_sets.get(lhs, set()))
        return follow_set

    def parse(self, sequence):
        sequence = sequence.split()
        stack = ['S']  # Assuming 'S' is the start symbol

        print(f"Parsing sequence: {sequence}")
        return self._parse_recursive(stack, sequence)

    def _parse_recursive(self, stack, sequence):
        if not stack and not sequence:
            return True
        if not stack or not sequence:
            return False

        top = stack.pop()
        if top == sequence[0]:
            print(f"Matched terminal: {top}")
            sequence.pop(0)
            return self._parse_recursive(stack, sequence)
        elif top in self.non_terminals:
            print(f"Expanding non-terminal: {top}")
            rules = self.grammar.get(top)
            if not rules:
                print(f"No production rules for non-terminal '{top}'.")
                return False
            for rule in rules:
                print(f"Trying production rule: {top} -> {rule}")
                new_stack = stack.copy()
                new_sequence = sequence.copy()
                new_stack.extend(reversed(rule.split()))
                if self._parse_recursive(new_stack, new_sequence):
                    return True
            return False
        else:
            print(f"Unexpected symbol: {top}")
            return False

    def run(self):
        while True:
            self.grammar.clear()
            self.terminals.clear()
            self.non_terminals.clear()
            self.first_sets.clear()
            self.follow_sets.clear()

            self.define_grammar()
            if not self.is_simple():
                print("The grammar is not simple. Please define a simple grammar.")
                continue
            self.compute_first_sets()
            self.compute_follow_sets()

            while True:
                print("\nOptions:")
                print("1. Define a new grammar.")
                print("2. Parse a sequence on current grammer.")
                print("3. Exit.")
                choice = input("Enter your choice: ").strip()

                if choice == '1':
                    break  # Go back to defining a new grammar
                elif choice == '2':
                    sequence = input("Enter the sequence to parse separated by space: ").strip()
                    if self.parse(sequence):
                        print("Sequence accepted.")
                    else:
                        print("Sequence rejected.")
                elif choice == '3':
                    print("Exiting the program.")
                    return
                else:
                    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    parser = TopDownParser()
    parser.run()
