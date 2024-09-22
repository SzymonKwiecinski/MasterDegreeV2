import pulp
import json

# Input data
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

# Problem parameters
K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Create the Linear Programming problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, upBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] +
               pulp.lpSum(recruit[k][i] for i in range(I)) -
               pulp.lpSum(overmanning[k][i] for i in range(I)) -
               pulp.lpSum(short[k][i] for i in range(I)) -
               (1 - data['lessonewaste'][k]) * data['strength'][k] * (1 - data['moreonewaste'][k])
               ) for k in range(K)) + \
               pulp.lpSum(data['costshort'][k] * short[k][i] for k in range(K) for i in range(I)) + \
               pulp.lpSum(data['costoverman'][k] * overmanning[k][i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        problem += (pulp.lpSum([recruit[k][j] for j in range(i + 1)]) +
                     (1 - data['lessonewaste'][k]) * data['strength'][k] +
                     (1 - data['moreonewaste'][k]) * data['strength'][k] -
                     pulp.lpSum(overmanning[k][j] for j in range(I)) -
                     pulp.lpSum(short[k][j] for j in range(I)) >= data['requirement'][k][i], f"Req_{k}_{i}")

# Solve the problem
problem.solve()

# Retrieve results
recruit_result = [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)]
overmanning_result = [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)]
short_result = [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]

# Output results
output = {
    "recruit": recruit_result,
    "overmanning": overmanning_result,
    "short": short_result
}
print(json.dumps(output))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')