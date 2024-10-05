import pulp

# Data input
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

# Problem setup
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision variables
translator_vars = {
    t['id']: pulp.LpVariable(f'x_{t["id"]}', cat='Binary')
    for t in data['translators']
}

# Objective function
problem += pulp.lpSum(t['cost'] * translator_vars[t['id']] for t in data['translators'])

# Constraints
for language in data['required_languages']:
    problem += pulp.lpSum(
        translator_vars[t['id']] for t in data['translators'] if language in t['languages']
    ) >= 1, f"Language_{language}_coverage"

# Solve the problem
problem.solve()

# Output the objective value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")