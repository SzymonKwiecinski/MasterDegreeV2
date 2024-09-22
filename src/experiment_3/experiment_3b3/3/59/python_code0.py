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

# Sets
translators = data['translators']
required_languages = data['required_languages']

# Create a list of translator IDs
translator_ids = [t['id'] for t in translators]

# Parameters
cost = {t['id']: t['cost'] for t in translators}
languages = {t['id']: t['languages'] for t in translators}

# Problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("select_translator", translator_ids, cat='Binary')

# Objective Function
problem += pulp.lpSum(cost[i] * x[i] for i in translator_ids), "Total Cost"

# Constraints
for language in required_languages:
    problem += pulp.lpSum(x[i] for i in translator_ids if language in languages[i]) >= 1, f"Coverage_{language}"

# Solve the problem
problem.solve()

# Output results
selected_translators = [i for i in translator_ids if x[i].value() == 1]
total_cost = pulp.value(problem.objective)

print(f'Selected Translators: {selected_translators}')
print(f'Total Cost: {total_cost}')
print(f'(Objective Value): <OBJ>{total_cost}</OBJ>')