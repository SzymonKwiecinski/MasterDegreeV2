import pulp
import json

# Data in JSON format
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

# Number of translators and required languages
N = len(data['translators'])
M = len(data['required_languages'])

# Create the optimization problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision variables: x_i
x = pulp.LpVariable.dicts("x", range(1, N + 1), cat='Binary')

# Objective Function
problem += pulp.lpSum([data['translators'][i - 1]['cost'] * x[i] for i in range(1, N + 1)]), "Total_Cost"

# Constraints: Each required language must be covered
for required_lang in data['required_languages']:
    problem += pulp.lpSum([x[i] for i in range(1, N + 1) if required_lang in data['translators'][i - 1]['languages']]) >= 1, f"Cover_{required_lang}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')