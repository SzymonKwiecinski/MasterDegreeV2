import pulp

# Input Data in JSON Format
data = {
    'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 
    'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']
}

# Define the problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Create decision variables
translator_vars = {translator['id']: pulp.LpVariable(f"translator_{translator['id']}", cat='Binary')
                   for translator in data['translators']}

# Objective Function: Minimize the total cost of selected translators
problem += pulp.lpSum(translator['cost'] * translator_vars[translator['id']]
                      for translator in data['translators'])

# Constraints: Ensure all required languages are covered
for language in data['required_languages']:
    problem += pulp.lpSum(translator_vars[translator['id']]
                          for translator in data['translators'] if language in translator['languages']) >= 1

# Solve the problem
problem.solve()

# Obtain results
selected_translators = [translator_id for translator_id, var in translator_vars.items() if pulp.value(var) == 1]
total_cost = sum(translator['cost'] for translator in data['translators'] if translator['id'] in selected_translators)

# Print solution in the specified output format
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)

# Print the objective function value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')