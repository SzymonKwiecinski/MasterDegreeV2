import pulp
import json

# Data from JSON
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
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Sets
translators = {t['id']: t for t in data['translators']}
required_languages = data['required_languages']

# Decision Variables
x = pulp.LpVariable.dicts('x', translators.keys(), cat=pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(translators[i]['cost'] * x[i] for i in translators), "Total_Cost"

# Constraints
for language in required_languages:
    problem += pulp.lpSum(x[i] for i in translators if language in translators[i]['languages']) >= 1, f"Coverage_{language}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')