import pulp
import json

data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Create the problem
problem = pulp.LpProblem("TranslatorAssignment", pulp.LpMinimize)

# Create decision variables
translators = {t['id']: pulp.LpVariable(f'x_{t["id"]}', cat='Binary') for t in data['translators']}

# Objective function: minimize total cost
problem += pulp.lpSum([t['cost'] * translators[t['id']] for t in data['translators']])

# Constraints: every required language must be covered
for language in data['required_languages']:
    problem += (pulp.lpSum([translators[t['id']] for t in data['translators'] if language in t['languages']]) >= 1, f"Cover_{language}")

# Solve the problem
problem.solve()

# Gather the results
selected_translators = [t.id for t in data['translators'] if pulp.value(translators[t['id']]) == 1]
total_cost = pulp.value(problem.objective)

# Output the result in the specified format
result = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')