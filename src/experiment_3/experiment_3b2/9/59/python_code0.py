import pulp

# Data from the provided JSON
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

# Parameters and sets
translators = data['translators']
required_languages = data['required_languages']
N = len(translators)
M = len(required_languages)

# Create a dictionary for language capabilities
lang = {(t['id'], lang): (1 if lang in t['languages'] else 0) for t in translators for lang in required_languages}

# Create the problem variable
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", [t['id'] for t in translators], cat='Binary')

# Objective function
problem += pulp.lpSum([t['cost'] * x[t['id']] for t in translators]), "Total_Cost"

# Constraints
for lang in required_languages:
    problem += pulp.lpSum([lang[(t['id'], lang)] * x[t['id']] for t in translators]) >= 1, f"Lang_{lang}_Coverage"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')