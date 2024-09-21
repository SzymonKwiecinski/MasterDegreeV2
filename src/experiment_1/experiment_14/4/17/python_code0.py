import pulp

# Data
data = {
    'translators': [
        {'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']},
        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']},
        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']},
        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']},
        {'id': 5, 'cost': 9000,  'languages': ['FR', 'GE', 'RU', 'SP']},
        {'id': 6, 'cost': 7000,  'languages': ['GE', 'SP', 'PO']}
    ],
    'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']
}

translators = data['translators']
required_languages = data['required_languages']

# Problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision Variables
translator_vars = pulp.LpVariable.dicts("hire", [t['id'] for t in translators], cat='Binary')

# Objective Function
problem += pulp.lpSum(t['cost'] * translator_vars[t['id']] for t in translators)

# Constraints
for lang in required_languages:
    problem += (
        pulp.lpSum(translator_vars[t['id']] for t in translators if lang in t['languages']) >= 1,
        f"Lang_{lang}_Coverage"
    )

# Solve
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')