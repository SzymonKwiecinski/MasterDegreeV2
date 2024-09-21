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

# Extracting data
translators = data['translators']
required_languages = data['required_languages']
N = len(translators)
M = len(required_languages)

# Creating the problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("hire", (i for i in range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(translators[i]['cost'] * x[i] for i in range(N))

# Constraints
for lang in required_languages:
    problem += pulp.lpSum(x[i] for i in range(N) if lang in translators[i]['languages']) >= 1

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')