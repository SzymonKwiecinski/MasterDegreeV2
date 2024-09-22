import pulp

# Input data
data = {
    "translators": [
        {"id": 1, "cost": 12000, "languages": ['FR', 'AR', 'IT']},
        {"id": 2, "cost": 16000, "languages": ['GE', 'RU', 'CH']},
        {"id": 3, "cost": 13000, "languages": ['AR', 'CH']},
        {"id": 4, "cost": 15000, "languages": ['FR', 'SP', 'IT', 'PO']},
        {"id": 5, "cost": 9000, "languages": ['FR', 'GE', 'RU', 'SP']},
        {"id": 6, "cost": 7000, "languages": ['GE', 'SP', 'PO']}
    ],
    "required_languages": ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']
}

# Define the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
translator_vars = {t['id']: pulp.LpVariable(f"translator_{t['id']}", cat='Binary') for t in data['translators']}

# Objective Function: Minimize total cost
problem += pulp.lpSum(translator_vars[t['id']] * t['cost'] for t in data['translators'])

# Constraint: Ensure all required languages are covered
for language in data['required_languages']:
    problem += pulp.lpSum(translator_vars[t['id']] for t in data['translators'] if language in t['languages']) >= 1

# Solve the problem
problem.solve()

# Extract the selected translators
selected_translators = [t['id'] for t in data['translators'] if translator_vars[t['id']].varValue == 1]

# Calculate the total cost
total_cost = sum(t['cost'] for t in data['translators'] if translator_vars[t['id']].varValue == 1)

# Output
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')