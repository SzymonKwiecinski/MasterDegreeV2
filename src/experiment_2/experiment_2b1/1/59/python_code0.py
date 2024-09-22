import pulp
import json

data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Extract data from the input
translators = data['translators']
required_languages = data['required_languages']

# Create a linear programming problem
problem = pulp.LpProblem("TranslatorSelection", pulp.LpMinimize)

# Create a dictionary for the decision variables
x = pulp.LpVariable.dicts("translator", [t['id'] for t in translators], cat='Binary')

# Objective function: minimize the total cost of selected translators
problem += pulp.lpSum([t['cost'] * x[t['id']] for t in translators]), "Total Cost"

# Constraints to ensure all required languages are covered
for lang in required_languages:
    problem += pulp.lpSum([x[t['id']] for t in translators if lang in t['languages']]) >= 1, f"Cover_{lang}"

# Solve the problem
problem.solve()

# Collect the selected translators
selected_translators = [t['id'] for t in translators if pulp.value(x[t['id']]) == 1]
total_cost = pulp.value(problem.objective)

# Output the selected translators and total cost
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')