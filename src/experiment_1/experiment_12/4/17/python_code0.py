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
translator_costs = {t['id']: t['cost'] for t in data['translators']}
translator_languages = {t['id']: t['languages'] for t in data['translators']}
required_languages = data['required_languages']

# Problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("hire", range(1, N+1), cat='Binary')

# Objective Function
problem += pulp.lpSum(translator_costs[i] * x[i] for i in range(1, N+1))

# Constraints
for lang in required_languages:
    problem += pulp.lpSum(x[i] for i in range(1, N+1) if lang in translator_languages[i]) >= 1, f"Cover_{lang}"

# Solve
problem.solve()

# Results
print(f"Status: {pulp.LpStatus[problem.status]}")
for i in range(1, N+1):
    if pulp.value(x[i]) == 1:
        print(f"Translator {i} is hired.")

print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')