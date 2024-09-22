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

# Create the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Create decision variables
translator_vars = {translator['id']: pulp.LpVariable(f"translator_{translator['id']}", cat='Binary') for translator in data['translators']}

# Objective function: Minimize the cost
problem += pulp.lpSum([translator['cost'] * translator_vars[translator['id']] for translator in data['translators']])

# Constraints: Ensure all required languages are covered
for language in data['required_languages']:
    problem += pulp.lpSum([translator_vars[translator['id']] for translator in data['translators'] if language in translator['languages']]) >= 1

# Solve the problem
problem.solve()

# Gather results
selected_translators = [translator_id for translator_id in translator_vars if translator_vars[translator_id].value() == 1]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')