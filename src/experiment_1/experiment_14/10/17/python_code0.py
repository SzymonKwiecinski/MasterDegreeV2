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

# Parameters
N = len(data['translators'])
M = len(data['required_languages'])
Costs = {translator['id']: translator['cost'] for translator in data['translators']}
Languages = {translator['id']: translator['languages'] for translator in data['translators']}
RequiredLanguages = data['required_languages']

# Initialize the problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Hire", [translator['id'] for translator in data['translators']], cat='Binary')

# Objective Function
problem += pulp.lpSum(Costs[i] * x[i] for i in range(1, N + 1)), "Total Hiring Cost"

# Constraints
for j in RequiredLanguages:
    # Each language must be covered by at least one translator
    problem += pulp.lpSum(x[i] for i in range(1, N + 1) if j in Languages[i]) >= 1, f"Cover_{j}"

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')