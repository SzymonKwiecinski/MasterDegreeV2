import pulp

# Data
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

K = len(data['requirement'])
I = len(data['requirement'][0])

# Problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costoverman'][k] * overmanning[k, i] + data['costshort'][k] * short[k, i] 
                      for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        problem += (
            data['strength'][k] +
            pulp.lpSum(recruit[k, j] * (1 - data['lessonewaste'][k]) + data['requirement'][k][j] * (1 - data['moreonewaste'][k]) 
                       for j in range(i)) +
            recruit[k, i] >=
            data['requirement'][k][i] + overmanning[k, i] + 0.5 * short[k, i]
        )

        problem += recruit[k, i] <= data['recruit'][k]
        problem += short[k, i] <= data['num_shortwork']

for i in range(I):
    problem += pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman']

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')