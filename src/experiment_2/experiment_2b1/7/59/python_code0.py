import json
import pulp

# Data input
data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, 
                         {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, 
                         {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, 
                         {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, 
                         {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, 
                         {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 
        'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Create the Linear Programming problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Create a binary variable for each translator
translator_vars = pulp.LpVariable.dicts("Translator", 
                                         [t['id'] for t in data['translators']], 
                                         0, 1, pulp.LpBinary)

# Objective function: Minimize the total cost
problem += pulp.lpSum([t['cost'] * translator_vars[t['id']] for t in data['translators']])

# Constraints to cover all required languages
for language in data['required_languages']:
    problem += pulp.lpSum([translator_vars[t['id']] for t in data['translators'] if language in t['languages']]) >= 1

# Solve the problem
problem.solve()

# Collect the selected translators and the total cost
selected_translators = [t['id'] for t in data['translators'] if pulp.value(translator_vars[t['id']]) == 1]
total_cost = pulp.value(problem.objective)

# Output the result
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

# Print the result
print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')