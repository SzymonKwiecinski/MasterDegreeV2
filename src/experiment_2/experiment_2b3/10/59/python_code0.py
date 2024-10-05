import pulp

# Problem data
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

# Define the problem
problem = pulp.LpProblem("Minimize_Translation_Cost", pulp.LpMinimize)

# Decision variables
x_vars = {translator['id']: pulp.LpVariable(f"x_{translator['id']}", cat='Binary') for translator in data['translators']}

# Objective function
problem += pulp.lpSum(translator['cost'] * x_vars[translator['id']] for translator in data['translators'])

# Constraints
covered_languages = {language: [] for language in data['required_languages']}
for translator in data['translators']:
    for lang in translator['languages']:
        if lang in covered_languages:
            covered_languages[lang].append(translator['id'])

for lang, translators in covered_languages.items():
    problem += pulp.lpSum(x_vars[trans_id] for trans_id in translators) >= 1

# Solve the problem
problem.solve()

# Output results
selected_translators = [translator['id'] for translator in data['translators'] if pulp.value(x_vars[translator['id']]) == 1]
total_cost = pulp.value(problem.objective)

output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')