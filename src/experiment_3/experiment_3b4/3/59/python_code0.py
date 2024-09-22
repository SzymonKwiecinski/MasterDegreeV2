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

# Set of translators and required languages
N = list(range(len(data['translators'])))
M = data['required_languages']

# Parameters
cost = {i: data['translators'][i]['cost'] for i in N}
languages = {i: data['translators'][i]['languages'] for i in N}

# Decision Variables
x = pulp.LpVariable.dicts('x', N, lowBound=0, cat='Binary')

# Problem
problem = pulp.LpProblem('TranslatorSelection', pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(cost[i] * x[i] for i in N), "Total Cost"

# Constraints
for j in M:
    problem += pulp.lpSum(x[i] for i in N if j in languages[i]) >= 1, f"Cover_{j}"

# Solving the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')