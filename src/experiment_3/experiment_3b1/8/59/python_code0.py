import pulp
import json

# Data in JSON format
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

# Initialize the problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision variables
translator_vars = {translator['id']: pulp.LpVariable(f"x_{translator['id']}", cat='Binary')
                   for translator in data['translators']}

# Objective Function
problem += pulp.lpSum(translator['cost'] * translator_vars[translator['id']] for translator in data['translators']), "Total_Cost"

# Constraints
for language in data['required_languages']:
    problem += (pulp.lpSum(translator_vars[translator['id']] 
                           for translator in data['translators'] 
                           if language in translator['languages']) >= 1), f"Lang_Coverage_{language}"

# Solve the problem
problem.solve()

# Extract selected translators and total cost
selected_translators = [translator['id'] for translator in data['translators'] if translator_vars[translator['id']].varValue == 1]
total_cost = pulp.value(problem.objective)

# Output results
print(f'Selected Translators: {selected_translators}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')