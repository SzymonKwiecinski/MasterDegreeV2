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

# Extract translators and languages
translators = data['translators']
required_languages = data['required_languages']
translator_ids = [t['id'] for t in translators]
costs = {t['id']: t['cost'] for t in translators}
language_coverage = {t['id']: t['languages'] for t in translators}

# Create the problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", translator_ids, cat='Binary')

# Objective function
problem += pulp.lpSum(costs[i] * x[i] for i in translator_ids), "Total_Cost"

# Constraints
for lang in required_languages:
    problem += pulp.lpSum(x[i] for i in translator_ids if lang in language_coverage[i]) >= 1, f"Cover_{lang}"

# Solve the problem
problem.solve()

# Outputs
selected_translators = [i for i in translator_ids if x[i].varValue == 1]
total_cost = pulp.value(problem.objective)

print(f'Selected Translators: {selected_translators}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')