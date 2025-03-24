class LeftRecursionEliminator:
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
                for Aj_prod in self.new_grammar.get(Aj, []):  
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
