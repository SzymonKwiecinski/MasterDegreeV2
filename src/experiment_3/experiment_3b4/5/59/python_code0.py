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

# Extracting data
translators = data['translators']
languages = data['required_languages']

# Creating a dictionary of costs
costs = {t['id']: t['cost'] for t in translators}

# Creating a dictionary to map translators to languages they can translate
language_matrix = {l: {t['id']: (1 if l in t['languages'] else 0) for t in translators} for l in languages}

# Initialize the Linear Programming problem
problem = pulp.LpProblem("MinimizeHiringCost", pulp.LpMinimize)

# Decision variables
x_vars = {t['id']: pulp.LpVariable(f"x_{t['id']}", cat='Binary') for t in translators}

# Objective function
problem += pulp.lpSum(costs[i] * x_vars[i] for i in x_vars)

# Constraints
for l in languages:
    problem += pulp.lpSum(language_matrix[l][i] * x_vars[i] for i in x_vars) >= 1

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')