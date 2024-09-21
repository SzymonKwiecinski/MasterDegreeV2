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
required_languages = data['required_languages']

# Problem
problem = pulp.LpProblem("HiringTranslators", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("HireTranslator", range(1, N+1), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['translators'][i-1]['cost'] * x[i] for i in range(1, N+1))

# Constraints
language_covered_constraints = {lang: pulp.lpSum(x[i] for i in range(1, N+1) if lang in data['translators'][i-1]['languages']) >= 1 for lang in required_languages}
for constraint in language_covered_constraints.values():
    problem += constraint

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')