import pulp
import json

# Data extracted from the provided JSON format
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

# Sets and parameters
translators = data['translators']
required_languages = data['required_languages']

# Create a list of translator IDs and a dictionary for their costs and language capabilities
T = [trans['id'] for trans in translators]
c = {trans['id']: trans['cost'] for trans in translators}
A = {trans['id']: [1 if lang in trans['languages'] else 0 for lang in required_languages] for trans in translators}

# Create the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", T, cat='Binary')

# Objective function
problem += pulp.lpSum(c[i] * x[i] for i in T)

# Constraints to ensure all required languages are covered
for l in range(len(required_languages)):
    problem += pulp.lpSum(A[i][l] * x[i] for i in T) >= 1

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')