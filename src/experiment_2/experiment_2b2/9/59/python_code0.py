import pulp

# The data from the problem description
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

# Create the problem instance
problem = pulp.LpProblem("MinCostTranslatorSelection", pulp.LpMinimize)

# Decision variables: 1 if translator i is selected, 0 otherwise
translator_vars = {translator['id']: pulp.LpVariable(f"t_{translator['id']}", cat='Binary') for translator in data['translators']}

# Objective: Minimize the total cost of selected translators
problem += pulp.lpSum(translator['cost'] * translator_vars[translator['id']] for translator in data['translators'])

# Constraints: Each required language must be covered by at least one selected translator
for language in data['required_languages']:
    problem += pulp.lpSum(translator_vars[translator['id']] 
                          for translator in data['translators'] if language in translator['languages']) >= 1

# Solve the problem
problem.solve()

# Extracting results
selected_translators = [translator['id'] for translator in data['translators'] if translator_vars[translator['id']].value() == 1]
total_cost = sum(translator['cost'] for translator in data['translators'] if translator_vars[translator['id']].value() == 1)

# Output
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')