import pulp

# Parse the input data
data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

translators = data['translators']
required_languages = set(data['required_languages'])

# Create the problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Define decision variables
trans_vars = pulp.LpVariable.dicts(
    "Translator", 
    [trans['id'] for trans in translators],
    cat='Binary'
)

# Objective function: minimize the total cost
problem += pulp.lpSum([trans_vars[trans['id']] * trans['cost'] for trans in translators])

# Constraints: Ensure all required languages are covered
for language in required_languages:
    problem += pulp.lpSum([trans_vars[trans['id']] for trans in translators if language in trans['languages']]) >= 1

# Solve the problem
problem.solve()

# Extract the selected translators and total cost
selected_translators = [trans['id'] for trans in translators if trans_vars[trans['id']].varValue == 1]
total_cost = sum(trans['cost'] for trans in translators if trans_vars[trans['id']].varValue == 1)

# Print results
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')