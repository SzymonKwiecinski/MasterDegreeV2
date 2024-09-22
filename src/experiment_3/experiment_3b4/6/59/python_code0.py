import pulp

# Data
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
N = len(data['translators'])
M = len(data['required_languages'])

# Parameters
cost = {translator['id']: translator['cost'] for translator in data['translators']}
a = {(translator['id'], lang): (1 if lang in translator['languages'] else 0) 
     for translator in data['translators'] 
     for lang in data['required_languages']}

# Problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", [translator['id'] for translator in data['translators']], 
                          cat='Binary')

# Objective Function
problem += pulp.lpSum(cost[i] * x[i] for i in range(1, N+1))

# Constraints
for lang in data['required_languages']:
    problem += pulp.lpSum(a[(i, lang)] * x[i] for i in range(1, N+1)) >= 1

# Solve
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')