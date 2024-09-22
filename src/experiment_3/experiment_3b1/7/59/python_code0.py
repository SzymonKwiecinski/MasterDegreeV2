import pulp
import json

# Data provided in JSON format
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
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Define decision variables
translator_ids = range(1, len(data['translators']) + 1)
x = pulp.LpVariable.dicts("x", translator_ids, cat='Binary')

# Objective function: Minimize total cost
problem += pulp.lpSum(data['translators'][i - 1]['cost'] * x[i] for i in translator_ids), "Total_Cost"

# Constraints: Ensure all required languages are covered
for language in data['required_languages']:
    problem += pulp.lpSum(x[i] for i in translator_ids if language in data['translators'][i - 1]['languages']) >= 1, f"Cover_{language}"

# Solve the problem
problem.solve()

# Output the results
selected_translators = [i for i in translator_ids if pulp.value(x[i]) == 1]
total_cost = pulp.value(problem.objective)

print(f'Selected Translators: {selected_translators}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')