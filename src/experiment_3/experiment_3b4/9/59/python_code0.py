import pulp

# Data from JSON format
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
N = len(data['translators'])  # Number of translators
required_languages = data['required_languages']

# Problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, N + 1), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['translators'][i]['cost'] * x[i + 1] for i in range(N))

# Constraints
for language in required_languages:
    problem += pulp.lpSum(
        x[i['id']] for i in data['translators'] if language in i['languages']
    ) >= 1, f"Cover_{language}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')