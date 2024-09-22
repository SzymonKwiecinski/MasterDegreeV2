import pulp

# Parsing the data
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

translators = data['translators']
required_languages = data['required_languages']

# Step 1: Define the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Step 2: Define the decision variables
translator_vars = pulp.LpVariable.dicts("Translator", [translator['id'] for translator in translators], cat='Binary')

# Step 3: Define the objective function
total_cost = pulp.lpSum(translator['cost'] * translator_vars[translator['id']] for translator in translators)
problem += total_cost

# Step 4: Define the constraints
for language in required_languages:
    problem += pulp.lpSum(translator_vars[translator['id']]
                          for translator in translators if language in translator['languages']) >= 1

# Step 5: Solve the problem
problem.solve()

# Step 6: Retrieve the solution
selected_translators = [translator['id'] for translator in translators if translator_vars[translator['id']].value() == 1]
total_cost = pulp.value(problem.objective)

# Output result
result = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')