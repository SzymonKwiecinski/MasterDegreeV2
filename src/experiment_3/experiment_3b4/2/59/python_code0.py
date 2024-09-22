import pulp

# Data from JSON
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

# Sets
T = [translator['id'] for translator in data['translators']]
L = data['required_languages']

# Parameters
cost = {translator['id']: translator['cost'] for translator in data['translators']}
a = {translator['id']: {lang: 0 for lang in L} for translator in data['translators']}

for translator in data['translators']:
    for lang in translator['languages']:
        a[translator['id']][lang] = 1

# Problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", T, cat=pulp.LpBinary)

# Objective function
problem += pulp.lpSum(cost[i] * x[i] for i in T)

# Constraints
for lang in L:
    problem += pulp.lpSum(a[i][lang] * x[i] for i in T) >= 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')