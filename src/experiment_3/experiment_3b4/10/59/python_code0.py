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

translators = data['translators']
required_languages = set(data['required_languages'])

# Define the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
x = {t['id']: pulp.LpVariable(f'x_{t["id"]}', cat='Binary') for t in translators}

# Objective function: Minimize the total cost
problem += pulp.lpSum(t['cost'] * x[t['id']] for t in translators), "Total_Cost"

# Constraints: Cover all required languages
for m in required_languages:
    problem += pulp.lpSum(x[t['id']] for t in translators if m in t['languages']) >= 1, f"Cover_{m}"

# Solve the problem
problem.solve()

# Print the result
print(f'Optimal Selection of Translators (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Selected Translators
selected_translators = [t['id'] for t in translators if x[t['id']].value() == 1]
print(f"Selected Translators: {selected_translators}")