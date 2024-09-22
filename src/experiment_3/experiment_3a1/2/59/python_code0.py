import pulp
import json

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

# Sets and Parameters
translators = data['translators']
required_languages = data['required_languages']

# Create the LP problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", [t['id'] for t in translators], cat='Binary')

# Objective Function
problem += pulp.lpSum([t['cost'] * x[t['id']] for t in translators]), "Total_Cost"

# Constraints
for language in required_languages:
    problem += pulp.lpSum([x[t['id']] for t in translators if language in t['languages']]) >= 1, f"Cover_{language}"

# Solve the problem
problem.solve()

# Output results
selected_translators = [t['id'] for t in translators if x[t['id']].value() == 1]
total_cost = pulp.value(problem.objective)

print(f'Selected Translators: {selected_translators}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')