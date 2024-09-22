import pulp

# Data from the provided json
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
N = len(translators)  # Number of translators

# Creating a Linear Programming problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Translator", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum([translators[i]['cost'] * x[i] for i in range(N)])

# Constraints
for language in required_languages:
    problem += pulp.lpSum([x[i] for i in range(N) if language in translators[i]['languages']]) >= 1

# Solve the problem
problem.solve()

# Output results
selected_translators = [translators[i]['id'] for i in range(N) if x[i].varValue == 1]
total_cost = pulp.value(problem.objective)

print("Selected Translators:", selected_translators)
print(f"Total Cost: {total_cost}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')