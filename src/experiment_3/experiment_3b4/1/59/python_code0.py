import pulp

# Data from the JSON
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

# Number of translators
N = len(data['translators'])

# Decision Variables
x = pulp.LpVariable.dicts('translator', range(N), cat='Binary')

# Problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(data['translators'][i]['cost'] * x[i] for i in range(N))

# Constraints
for lang in data['required_languages']:
    problem += (
        pulp.lpSum(x[i] for i in range(N) if lang in data['translators'][i]['languages']) >= 1,
        f"language_{lang}"
    )

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')