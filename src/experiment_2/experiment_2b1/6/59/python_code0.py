import pulp
import json

# Input data in JSON format
data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Extracting the data
translators = data['translators']
required_languages = data['required_languages']

# Creating the LP problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
x = {translator['id']: pulp.LpVariable(f"x_{translator['id']}", cat='Binary') for translator in translators}

# Objective function: minimize total cost
problem += pulp.lpSum(translator['cost'] * x[translator['id']] for translator in translators)

# Constraints: ensure all required languages are covered
for language in required_languages:
    problem += pulp.lpSum(x[translator['id']] for translator in translators if language in translator['languages']) >= 1

# Solve the problem
problem.solve()

# Collecting the results
selected_translators = [translator['id'] for translator in translators if pulp.value(x[translator['id']]) == 1]
total_cost = pulp.value(problem.objective)

# Output the results
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')