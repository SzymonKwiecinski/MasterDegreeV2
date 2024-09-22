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

# Extracting data
translators = data['translators']
required_languages = data['required_languages']
N = len(translators)
M = len(required_languages)

# Initialize the problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("translator", range(1, N + 1), cat='Binary')

# Objective function
problem += pulp.lpSum(translators[i-1]['cost'] * x[i] for i in range(1, N + 1))

# Constraints for required languages coverage
for language in required_languages:
    problem += pulp.lpSum(x[i] for i in range(1, N + 1) if language in translators[i-1]['languages']) >= 1

# Solve the problem
problem.solve()

# Getting outputs
selected_translators = [i for i in range(1, N + 1) if pulp.value(x[i]) == 1]
total_cost = pulp.value(problem.objective)

# Printing the results
print(f'Selected Translators: {selected_translators}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')