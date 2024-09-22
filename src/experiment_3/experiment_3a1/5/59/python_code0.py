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

# Extracting translators and required languages
translators = data['translators']
required_languages = data['required_languages']
N = len(translators)
M = len(required_languages)

# Initialize the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), cat='Binary')

# Objective function
problem += pulp.lpSum(translators[i]['cost'] * x[i] for i in range(N)), "Total_Cost"

# Constraints to ensure all required languages are covered
for language in required_languages:
    problem += pulp.lpSum(x[i] for i in range(N) if language in translators[i]['languages']) >= 1, f"Cover_{language}"

# Solve the problem
problem.solve()

# Extracting results
selected_translators = [translators[i]['id'] for i in range(N) if pulp.value(x[i]) == 1]
total_cost = pulp.value(problem.objective)

# Print results
print(f'Selected Translators: {selected_translators}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')