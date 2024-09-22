import pulp

# Data provided
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

# Initialize the problem
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("translator", [translator['id'] for translator in data['translators']], cat='Binary')

# Objective Function
problem += pulp.lpSum(translator['cost'] * x[translator['id']] for translator in data['translators'])

# Constraints
for lang in data['required_languages']:
    problem += pulp.lpSum(x[translator['id']] 
                          for translator in data['translators'] 
                          if lang in translator['languages']) >= 1, f"Cover_{lang}"

# Solve the problem
problem.solve()

# Extract results
selected_translators = [translator['id'] for translator in data['translators'] if x[translator['id']].varValue == 1]
total_cost = pulp.value(problem.objective)

# Display results
print(f"Selected Translators: {selected_translators}")
print(f"Total Cost: {total_cost}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')