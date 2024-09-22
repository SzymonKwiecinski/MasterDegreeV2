import pulp
import json

data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Define the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
x = {translator['id']: pulp.LpVariable(f"x_{translator['id']}", cat='Binary') for translator in data['translators']}

# Objective function
problem += pulp.lpSum([translator['cost'] * x[translator['id']] for translator in data['translators']])

# Constraints
for language in data['required_languages']:
    problem += pulp.lpSum([x[translator['id']] for translator in data['translators'] if language in translator['languages']]) >= 1

# Solve the problem
problem.solve()

# Collect the results
selected_translators = [translator_id for translator_id in x if x[translator_id].varValue == 1]
total_cost = pulp.value(problem.objective)

# Output format
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')