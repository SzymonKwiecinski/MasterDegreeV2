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

# Problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', 
                          [translator['id'] for translator in data['translators']], 
                          cat='Binary')

# Objective Function
problem += pulp.lpSum([translator['cost'] * x[translator['id']] for translator in data['translators']])

# Constraints
for language in data['required_languages']:
    problem += pulp.lpSum([x[translator['id']] 
                           for translator in data['translators'] 
                           if language in translator['languages']]) >= 1

# Solve
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')