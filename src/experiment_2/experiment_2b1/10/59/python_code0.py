import pulp
import json

# Input Data
data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, 
                        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, 
                        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, 
                        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, 
                        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, 
                        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 
        'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Model
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Variables
translator_vars = pulp.LpVariable.dicts("Translator", 
                                         [translator['id'] for translator in data['translators']], 
                                         cat='Binary')

# Objective Function
problem += pulp.lpSum(translator['cost'] * translator_vars[translator['id']] 
                       for translator in data['translators']), "Total_Cost"

# Constraints
for language in data['required_languages']:
    problem += pulp.lpSum(translator_vars[translator['id']] 
                           for translator in data['translators'] 
                           if language in translator['languages']) >= 1, f"Cover_{language}"

# Solve the problem
problem.solve()

# Output
selected_translators = [translator['id'] for translator in data['translators'] 
                        if translator_vars[translator['id']].varValue == 1]

total_cost = pulp.value(problem.objective)

# Format output
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

# Print result
print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')