from collections import defaultdict

def left_factor(grammar):
    new_grammar = {}
    created_non_terminals = set()

    for non_terminal, productions in grammar.items():
        prefix_map = defaultdict(list)
        
        for prod in productions:
            for i in range(1, len(prod) + 1):
                prefix_map[prod[:i]].append(prod)

        longest_common_prefix = ""
        for prefix, group in prefix_map.items():
            if len(group) > 1 and len(prefix) > len(longest_common_prefix):
                longest_common_prefix = prefix

        if not longest_common_prefix:
            new_grammar[non_terminal] = productions
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
        new_grammar[non_terminal] = [longest_common_prefix + new_non_terminal] + remaining_productions
        new_grammar[new_non_terminal] = factored_productions

    return new_grammar
