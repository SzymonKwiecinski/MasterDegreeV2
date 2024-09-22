import pulp
import json

# Input data
data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']},
                        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']},
                        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']},
                        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']},
                        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']},
                        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}],
        'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Problem definition
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Variables
translator_vars = pulp.LpVariable.dicts("Translators", [t['id'] for t in data['translators']], 
                                          cat='Binary')

# Objective function
problem += pulp.lpSum([t['cost'] * translator_vars[t['id']] for t in data['translators']])

# Constraints
for language in data['required_languages']:
    problem += pulp.lpSum([translator_vars[t['id']] for t in data['translators'] 
                           if language in t['languages']]) >= 1, f"Lang_{language}"

# Solve the problem
problem.solve()

# Selected translators and total cost
selected_translators = [t['id'] for t in data['translators'] if translator_vars[t['id']].value() == 1]
total_cost = pulp.value(problem.objective)

# Output format
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')