import pulp
import json

data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Extracting translators and required languages
translators = data['translators']
required_languages = data['required_languages']

# Create the optimization problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Create a binary variable for each translator
translator_vars = pulp.LpVariable.dicts("Select", [t['id'] for t in translators], cat='Binary')

# Objective function: minimize total cost
problem += pulp.lpSum([t['cost'] * translator_vars[t['id']] for t in translators])

# Constraints: all required languages must be covered
for lang in required_languages:
    problem += pulp.lpSum([translator_vars[t['id']] for t in translators if lang in t['languages']]) >= 1

# Solve the problem
problem.solve()

# Gather results
selected_translators = [t['id'] for t in translators if translator_vars[t['id']].varValue == 1]
total_cost = pulp.value(problem.objective)

output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')