import pulp

# Parse the data
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

# Define problem
problem = pulp.LpProblem("Hiring Translators", pulp.LpMinimize)

# Define decision variables
translator_vars = {
    translator['id']: pulp.LpVariable(f"x_{translator['id']}", cat='Binary')
    for translator in data['translators']
}

# Objective function: Minimize the total cost
problem += pulp.lpSum(translator['cost'] * translator_vars[translator['id']] for translator in data['translators'])

# Constraints: Each required language must be covered
for language in data['required_languages']:
    problem += pulp.lpSum(
        translator_vars[translator['id']]
        for translator in data['translators']
        if language in translator['languages']
    ) >= 1, f"Cover_{language}"

# Solve the problem
problem.solve()

# Display the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')