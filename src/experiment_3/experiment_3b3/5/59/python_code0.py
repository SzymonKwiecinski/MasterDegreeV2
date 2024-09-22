import pulp

# Data extraction
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

# Create the LP Problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Set of translators and costs
translator_vars = {
    t['id']: pulp.LpVariable(f"x_{t['id']}", cat='Binary') for t in translators
}

# Objective Function: Minimize the total cost
problem += pulp.lpSum(translator_vars[t['id']] * t['cost'] for t in translators)

# Constraints: Ensure all required languages are covered
for lang in required_languages:
    problem += pulp.lpSum(
        translator_vars[t['id']] * (1 if lang in t['languages'] else 0) 
        for t in translators
    ) >= 1

# Solve the problem
problem.solve()

# Output results
selected_translators = [t['id'] for t in translators if pulp.value(translator_vars[t['id']]) == 1]
total_cost = pulp.value(problem.objective)

print(f"Selected Translators: {selected_translators} (Objective Value): <OBJ>{total_cost}</OBJ>")