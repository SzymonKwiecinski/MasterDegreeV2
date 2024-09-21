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

# Parameters
N = len(data['translators'])
M = len(data['required_languages'])
costs = [translator['cost'] for translator in data['translators']]
languages = [set(translator['languages']) for translator in data['translators']]
required_languages = set(data['required_languages'])

# Problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum(costs[i] * x[i] for i in range(N)), "Total Hiring Cost"

# Constraints
for language in required_languages:
    problem += (pulp.lpSum(x[i] for i in range(N) if language in languages[i]) >= 1), f"Language_Coverage_{language}"

# Solve the problem
problem.solve()

# Output the results
print(f'Status: {pulp.LpStatus[problem.status]}')
for i in range(N):
    print(f'Translator {i + 1} hired: {x[i].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')