import pulp
import json

# Data input
data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, 
                        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, 
                        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, 
                        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, 
                        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, 
                        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 
         'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Problem definition
problem = pulp.LpProblem("TranslatorSelection", pulp.LpMinimize)

# Variables
translator_vars = {translator['id']: pulp.LpVariable(f"translator_{translator['id']}", cat='Binary')
                   for translator in data['translators']}

# Objective function
problem += pulp.lpSum(translator['cost'] * translator_vars[translator['id']] 
                       for translator in data['translators']), "Total_Cost"

# Constraints to ensure all required languages are covered
for lang in data['required_languages']:
    problem += pulp.lpSum(translator_vars[translator['id']] 
                           for translator in data['translators'] 
                           if lang in translator['languages']) >= 1, f"Cover_{lang}"

# Solve the problem
problem.solve()

# Collecting results
selected_translators = [translator['id'] for translator in data['translators'] 
                        if translator_vars[translator['id']].value() == 1]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')