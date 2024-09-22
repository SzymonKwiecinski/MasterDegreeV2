import pulp

# Data from JSON
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

# Parameters
K = len(data['requirement'])  # Categories of manpower
I = len(data['requirement'][0])  # Years

# Initialize Problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
hire = [[pulp.LpVariable(f"hire_{k}_{i}", 0, data['recruit'][k], cat='Integer') for i in range(I)] for k in range(K)]
redundancy = [[pulp.LpVariable(f"redundancy_{k}_{i}", 0, data['strength'][k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f"overmanning_{k}_{i}", 0, data['num_overman'], cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f"short_{k}_{i}", 0, data['num_shortwork'], cat='Integer') for i in range(I)] for k in range(K)]

# Objective Function
cost_of_redundancy = pulp.lpSum(data['costredundancy'][k] * redundancy[k][i] for k in range(K) for i in range(I))
cost_of_overmanning = pulp.lpSum(data['costoverman'][k] * overmanning[k][i] for k in range(K) for i in range(I))
cost_of_short = pulp.lpSum(data['costshort'][k] * short[k][i] for k in range(K) for i in range(I))
problem += cost_of_redundancy + cost_of_overmanning + cost_of_short

# Constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            # First year constraints
            problem += data['strength'][k] + hire[k][i] - redundancy[k][i] - (1 - data['moreonewaste'][k]) * data['strength'][k] >= \
                       data['requirement'][k][i] - overmanning[k][i] + 0.5 * short[k][i]
        else:
            # Subsequent years constraints
            prev_strength = data['strength'][k] if i == 1 else hire[k][i-1] * (1 - data['lessonewaste'][k])
            problem += prev_strength + hire[k][i] - redundancy[k][i] - (1 - data['moreonewaste'][k]) * prev_strength >= \
                       data['requirement'][k][i] - overmanning[k][i] + 0.5 * short[k][i]

# Solve the problem
problem.solve()

# Extract Results
output = {
    "recruit": [[int(hire[k][i].varValue) for i in range(I)] for k in range(K)],
    "overmanning": [[int(overmanning[k][i].varValue) for i in range(I)] for k in range(K)],
    "short": [[int(short[k][i].varValue) for i in range(I)] for k in range(K)],
}

print(output)

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')