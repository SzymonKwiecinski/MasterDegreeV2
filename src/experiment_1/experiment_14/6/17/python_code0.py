import pulp

# Data
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

# Extract necessary data
translators = data['translators']
required_languages = data['required_languages']

# Number of translators
N = len(translators)

# Create the problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("translator", range(1, N + 1), cat='Binary')

# Objective function: Minimize the total cost of hiring translators
problem += pulp.lpSum(translator['cost'] * x[translator['id']] for translator in translators)

# Constraints: Each required language must be covered by at least one hired translator
for lang in required_languages:
    problem += pulp.lpSum(x[translator['id']] for translator in translators if lang in translator['languages']) >= 1

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')