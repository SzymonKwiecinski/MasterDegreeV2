import pulp
import json

data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Extract data
translators = data['translators']
required_languages = data['required_languages']

# Create the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("Translators", [t['id'] for t in translators], cat='Binary')

# Objective function
problem += pulp.lpSum([t['cost'] * x[t['id']] for t in translators]), "Total_Cost"

# Constraints: Ensure all required languages are covered
for lang in required_languages:
    problem += pulp.lpSum([x[t['id']] for t in translators if lang in t['languages']]) >= 1, f"Coverage_{lang}"

# Solve the problem
problem.solve()

# Collecting the results
selected_translators = [t['id'] for t in translators if x[t['id']].varValue == 1]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}
print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')