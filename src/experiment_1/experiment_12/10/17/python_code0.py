import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision Variables
x = {
    translator['id']: pulp.LpVariable(f"x_{translator['id']}", cat='Binary')
    for translator in data['translators']
}

# Objective Function
problem += pulp.lpSum(translator['cost'] * x[translator['id']] for translator in data['translators'])

# Constraints
for language in data['required_languages']:
    problem += pulp.lpSum(
        x[translator['id']] for translator in data['translators'] if language in translator['languages']
    ) >= 1, f"Cover_language_{language}"

# Solve
problem.solve()

# Results
print("Status:", pulp.LpStatus[problem.status])
print("Selected Translators:")
for translator in data['translators']:
    if x[translator['id']].varValue == 1:
        print(f" - Translator {translator['id']} at cost {translator['cost']} can cover languages {translator['languages']}")

print(f"Total Cost (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")