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

# Constants
N = len(data['translators'])
M = len(data['required_languages'])

# Problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Hire", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['translators'][i]['cost'] * x[i] for i in range(N)), "Total_Hiring_Cost"

# Constraints
for language in data['required_languages']:
    problem += pulp.lpSum(x[i] for i in range(N) if language in data['translators'][i]['languages']) >= 1, f"Cover_{language}"

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')