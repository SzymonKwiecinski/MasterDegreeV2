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

# Problem setup
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
translators = {translator['id']: pulp.LpVariable(f"x_{translator['id']}", cat='Binary') for translator in data['translators']}

# Objective function
problem += pulp.lpSum(translator['cost'] * translators[translator['id']] for translator in data['translators'])

# Constraints to cover all required languages
for language in data['required_languages']:
    problem += pulp.lpSum(translators[translator['id']] for translator in data['translators'] if language in translator['languages']) >= 1

# Solve the problem
problem.solve()

# Gather selected translators
selected_translators = [translator['id'] for translator in data['translators'] if pulp.value(translators[translator['id']]) == 1]
total_cost = pulp.value(problem.objective)

# Output result
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')