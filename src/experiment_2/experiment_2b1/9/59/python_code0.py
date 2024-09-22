import pulp
import json

data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Create the optimization problem
problem = pulp.LpProblem("TranslatorSelection", pulp.LpMinimize)

# Decision variables
translators = {t['id']: pulp.LpVariable(f'Translator_{t["id"]}', cat='Binary') for t in data['translators']}

# Objective function
problem += pulp.lpSum([t['cost'] * translators[t['id']] for t in data['translators']]), "Total_Cost"

# Constraints
for lang in data['required_languages']:
    problem += pulp.lpSum([translators[t['id']] for t in data['translators'] if lang in t['languages']]) >= 1, f"Cover_{lang}"

# Solve the problem
problem.solve()

# Prepare the output
selected_translators = [t['id'] for t in data['translators'] if pulp.value(translators[t['id']]) == 1]
total_cost = pulp.value(problem.objective)

output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')