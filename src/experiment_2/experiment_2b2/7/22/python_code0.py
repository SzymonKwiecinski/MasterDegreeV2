import pulp

# Problem data
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

K = len(data['requirement'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Variables
recruit = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), 0)
overmanning = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), 0)
short = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), 0)
redundancy = pulp.LpVariable.dicts("Redundancy", ((k, i) for k in range(K) for i in range(I)), 0)

# Objective: Minimize redundancy cost
problem += pulp.lpSum(data['costredundancy'][k] * redundancy[(k, i)] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    workers = data['strength'][k]
    for i in range(I):
        requirement = data['requirement'][k][i]

        # Calculate wastage
        new_wastage = (1 - data['lessonewaste'][k]) * recruit[(k, i-1)] if i > 0 else 0
        existing_wastage = (1 - data['moreonewaste'][k]) * (workers - recruit[(k, i-1)]) if i > 0 else workers

        # Update available manpower after wastage
        workers = new_wastage + existing_wastage + recruit[(k, i)] - redundancy[(k, i)] + overmanning[(k, i)]

        # Constraint for manpower requirement
        problem += workers + 0.5 * short[(k, i)] >= requirement

        # Constraint for recruitment limits
        problem += recruit[(k, i)] <= data['recruit'][k]

        # Constraint for overmanning limits
        problem += overmanning[(k, i)] <= data['num_overman'] / K

        # Constraint for short working time limits
        problem += short[(k, i)] <= data['num_shortwork']

# Solving the problem
problem.solve()

# Building the output
output = {
    "recruit": [[pulp.value(recruit[(k, i)]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[(k, i)]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[(k, i)]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')