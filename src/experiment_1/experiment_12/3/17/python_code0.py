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

# Create a LP problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('translator', range(1, N + 1), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['translators'][i]['cost'] * x[i + 1] for i in range(N)), "Total Cost"

# Constraints
for language in data['required_languages']:
    problem += pulp.lpSum(
        x[translator['id']] for translator in data['translators'] if language in translator['languages']
    ) >= 1, f"Coverage_for_{language}"

# Solve the problem
problem.solve()

# Output the results
print(f"Status: {pulp.LpStatus[problem.status]}")
for i in range(1, N + 1):
    if pulp.value(x[i]) == 1:
        print(f"Translator {i} is hired.")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')