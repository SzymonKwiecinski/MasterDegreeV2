import pulp

# Data extracted from the JSON-like structure
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

K = len(data['strength'])
I = len(data['requirement'][0])

# Create the optimization problem
problem = pulp.LpProblem("Minimize_Redundancy_Cost", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * redundancy[(k, i)] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    current = {}
    for i in range(I):
        # Workforce balance
        if i == 0:
            current[i] = data['strength'][k]
        else:
            current[i] = current[i-1] * (1 - data['moreonewaste'][k]) + recruit[(k, i-1)]

        # Manpower utilization
        problem += current[i] + overmanning[(k, i)] == data['requirement'][k][i] - short[(k, i)] / 2 + redundancy[(k, i)]

        # Recruitment limit
        problem += recruit[(k, i)] <= data['recruit'][k]

        # Short-time working limit
        problem += short[(k, i)] <= data['num_shortwork']

# Overmanning limit
for i in range(I):
    problem += pulp.lpSum(overmanning[(k, i)] for k in range(K)) <= data['num_overman']

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')