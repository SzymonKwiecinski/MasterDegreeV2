import pulp
import json

# Given data
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

# Extracting translators data
translators = data['translators']
required_languages = data['required_languages']

# Create the problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("Translator", [trans['id'] for trans in translators], cat='Binary')

# Objective function
problem += pulp.lpSum(trans['cost'] * x[trans['id']] for trans in translators), "Total_Cost"

# Constraints
for language in required_languages:
    problem += pulp.lpSum(x[trans['id']] for trans in translators if language in trans['languages']) >= 1, f"Cover_{language}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')