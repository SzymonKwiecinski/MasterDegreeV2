import pulp
import json

# Input data
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

# Create the optimization problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
translator_vars = pulp.LpVariable.dicts("Translator", [translator['id'] for translator in data['translators']], cat='Binary')

# Objective function: Minimize the total cost of selected translators
problem += pulp.lpSum([translator['cost'] * translator_vars[translator['id']] for translator in data['translators']])

# Constraints: Ensure all required languages are covered
for language in data['required_languages']:
    problem += pulp.lpSum([translator_vars[translator['id']] for translator in data['translators'] if language in translator['languages']]) >= 1

# Solve the problem
problem.solve()

# Get the selected translators and total cost
selected_translators = [translator['id'] for translator in data['translators'] if translator_vars[translator['id']].varValue == 1]
total_cost = pulp.value(problem.objective)

# Output results
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')