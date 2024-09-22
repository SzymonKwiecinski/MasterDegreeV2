import pulp

# Data from json
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
lang = {(translator['id'], language): 1 if language in translator['languages'] else 0
        for translator in data['translators'] for language in L}

# Problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", T, cat='Binary')

# Objective Function
problem += pulp.lpSum(cost[i] * x[i] for i in T), "Total_Cost"

# Constraints
for j in L:
    problem += pulp.lpSum(lang[(i, j)] * x[i] for i in T) >= 1, f"Language_{j}_Coverage"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')