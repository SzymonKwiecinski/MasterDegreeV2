import pulp

# Parse the input data
data = {
    'translators': [
        {'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']},
        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']},
        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']},
        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']},
        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']},
        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}
    ],
    'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']
}

translators = data['translators']
required_languages = data['required_languages']

# Define the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Define decision variables
translator_vars = pulp.LpVariable.dicts("Translator", 
                                        [t['id'] for t in translators], 
                                        cat='Binary')

# Objective function: minimize total cost
problem += pulp.lpSum([t['cost'] * translator_vars[t['id']] for t in translators])

# Constraints: cover all required languages
for language in required_languages:
    problem += pulp.lpSum(translator_vars[t['id']] 
                          for t in translators 
                          if language in t['languages']) >= 1, f"Cover_{language}"

# Solve the problem
problem.solve()

# Retrieve the results
selected_translators = [t['id'] for t in translators if pulp.value(translator_vars[t['id']]) == 1]
total_cost = sum(t['cost'] for t in translators if pulp.value(translator_vars[t['id']]) == 1)

# Output format
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')