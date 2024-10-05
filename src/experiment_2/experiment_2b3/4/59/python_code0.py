import pulp

# Data
data = {
    'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']},
                    {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']},
                    {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']},
                    {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']},
                    {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']},
                    {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}],
    'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']
}

# Creating the MILP problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision variables
translator_vars = pulp.LpVariable.dicts("Translator", 
                                        [translator['id'] for translator in data['translators']], 
                                        cat=pulp.LpBinary)

# Objective function: Minimize the total cost
problem += pulp.lpSum(translator['cost'] * translator_vars[translator['id']] for translator in data['translators'])

# Constraints: Ensure every required language is covered
for language in data['required_languages']:
    problem += pulp.lpSum(translator_vars[translator['id']] 
                          for translator in data['translators'] if language in translator['languages']) >= 1, f"Coverage_{language}"

# Solve the problem
problem.solve()

# Prepare and print the output
selected_translators = [t['id'] for t in data['translators'] if translator_vars[t['id']].value() == 1]
total_cost = sum(t['cost'] for t in data['translators'] if translator_vars[t['id']].value() == 1)

output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')