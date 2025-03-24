from collections import defaultdict

class GrammarProcessor:
    def __init__(self, grammar):
        self.grammar = grammar  # Input grammar
        self.non_terminals = list(grammar.keys())  # List of non-terminals
        self.new_grammar = {}  # Stores transformed grammar

    def eliminate_left_recursion(self):
        """Eliminates both direct and indirect left recursion."""
        for i in range(len(self.non_terminals)):
            Ai = self.non_terminals[i]
            
            # Step 1: Substitute indirect left recursion
            for j in range(i):
                Aj = self.non_terminals[j]
                self.substitute_indirect_recursion(Ai, Aj)
            
            # Step 2: Eliminate direct left recursion in Ai
            self.remove_direct_left_recursion(Ai)
        
        return self.new_grammar

    def substitute_indirect_recursion(self, Ai, Aj):
        """Replaces Ai → Ajγ with Aj's productions to remove indirect recursion."""
        new_productions = []
        for prod in self.grammar[Ai]:
            if prod.startswith(Aj):  # Ai → Ajγ detected
                for Aj_prod in self.new_grammar[Aj]:  
                    new_productions.append(Aj_prod + prod[len(Aj):])  # Replace Aj with its productions
            else:
                new_productions.append(prod)
        self.grammar[Ai] = new_productions  # Update Ai's rules

    def remove_direct_left_recursion(self, non_terminal):
        """Removes direct left recursion for a given non-terminal."""
        productions = self.grammar[non_terminal]
        alpha = []  # Recursive parts (A → Aα)
        beta = []   # Non-recursive parts (A → β)

        for prod in productions:
            if prod.startswith(non_terminal):  
                alpha.append(prod[len(non_terminal):])  # Extract α
            else:
                beta.append(prod)  # Store β
        
        if not alpha:  
            self.new_grammar[non_terminal] = productions  # No left recursion
            return

        # New non-terminal A'
        new_non_terminal = non_terminal + "'"
        
        # Update grammar with transformed rules
        self.new_grammar[non_terminal] = [b + new_non_terminal for b in beta]  # A → βA'
        self.new_grammar[new_non_terminal] = [a + new_non_terminal for a in alpha] + ["ε"]  # A' → αA' | ε

def left_factor(self):
    """Performs left factoring on the grammar."""
    factored_grammar = {}
    created_non_terminals = set()

    for non_terminal, productions in self.grammar.items():  # Use self.grammar
        prefix_map = defaultdict(list)
        
        for prod in productions:
            for i in range(1, len(prod) + 1):
                prefix_map[prod[:i]].append(prod)

        longest_common_prefix = ""
        for prefix, group in prefix_map.items():
            if len(group) > 1 and len(prefix) > len(longest_common_prefix):
                longest_common_prefix = prefix

        if not longest_common_prefix:
            factored_grammar[non_terminal] = productions
            continue

        new_non_terminal = non_terminal + "'"
        while new_non_terminal in created_non_terminals:
            new_non_terminal += "'"
        created_non_terminals.add(new_non_terminal)

        factored_productions = []
        remaining_productions = []
        
        for prod in productions:
            if prod.startswith(longest_common_prefix):
                remaining_part = prod[len(longest_common_prefix):]
                factored_productions.append(remaining_part if remaining_part else 'ε')
            else:
                remaining_productions.append(prod)
        factored_grammar[non_terminal] = [longest_common_prefix + new_non_terminal] + remaining_productions
        factored_grammar[new_non_terminal] = factored_productions

    return factored_grammar


def get_user_grammar():
    """Gets user input to define the grammar."""
    grammar = defaultdict(list)
    n = int(input("Enter the number of non-terminals: "))

    for _ in range(n):
        non_terminal = input("Enter non-terminal: ").strip()
        productions = input(f"Enter productions for {non_terminal} (separated by '|'): ").split('|')
        grammar[non_terminal] = [p.strip() for p in productions]

    return grammar

if __name__ == "__main__":
    print("Enter the context-free grammar:")
    grammar = get_user_grammar()
    
    processor = GrammarProcessor(grammar)
    
    print("\nChoose an option:")
    print("1. Eliminate Left Recursion")
    print("2. Perform Left Factoring")
    choice = int(input("Enter your choice (1/2): "))
    
    if choice == 1:
        transformed_grammar = processor.eliminate_left_recursion()
        print("\nGrammar after Eliminating Left Recursion:")
        for nt, rules in transformed_grammar.items():
            print(f"{nt} -> {' | '.join(rules)}")
    elif choice == 2:
        factored_grammar = processor.left_factor()
        print("\nGrammar after Left Factoring:")
        for nt, rules in factored_grammar.items():
            print(f"{nt} -> {' | '.join(rules)}")
    else:
        print("Invalid choice. Please enter 1 or 2.")
