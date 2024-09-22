import pulp

# Define the data
data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Extract translators data
translators = data['translators']
required_languages = data['required_languages']

# Create the problem
problem = pulp.LpProblem("Minimize_Translation_Cost", pulp.LpMinimize)

# Variables: whether to select a translator
translator_vars = {translator['id']: pulp.LpVariable(f"select_translator_{translator['id']}", cat='Binary') for translator in translators}

# Objective: Minimize total cost
problem += pulp.lpSum(translator['cost'] * translator_vars[translator['id']] for translator in translators)

# Constraints: Ensure each required language is covered
for language in required_languages:
    problem += pulp.lpSum(translator_vars[translator['id']] for translator in translators if language in translator['languages']) >= 1, f"Ensure_language_{language}"

# Solve the problem
problem.solve()

# Gather results
selected_translators = [translator['id'] for translator in translators if pulp.value(translator_vars[translator['id']]) == 1]
total_cost = sum(translator['cost'] for translator in translators if pulp.value(translator_vars[translator['id']]) == 1)

# Output results
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')