import pulp

# Define the data
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

# Extract data
translators = data['translators']
required_languages = data['required_languages']

# Create a problem instance
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Define decision variables
translator_vars = {t['id']: pulp.LpVariable(f"translator_{t['id']}", cat='Binary') for t in translators}

# Define the objective function
problem += pulp.lpSum(translator_vars[t['id']] * t['cost'] for t in translators), "Total_Cost"

# Define constraints
for lang in required_languages:
    problem += pulp.lpSum(translator_vars[t['id']] for t in translators if lang in t['languages']) >= 1, f"language_{lang}"

# Solve the problem
problem.solve()

# Prepare the output
selected_translators = [t['id'] for t in translators if translator_vars[t['id']].varValue == 1]
total_cost = pulp.value(problem.objective)

output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')