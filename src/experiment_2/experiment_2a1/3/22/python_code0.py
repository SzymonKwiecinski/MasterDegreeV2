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

# Problem data
K = len(data['requirement'])       # Number of manpower types
I = len(data['requirement'][0])    # Number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=lambda k: data['recruit'][k], cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=data['num_shortwork'], cat='Integer')

# Objective function
cost_redundancy = pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i] - overmanning[(k, i)] - short[(k, i) / 2]) 
                              for k in range(K) for i in range(I))
problem += cost_redundancy, "Total_Redundancy_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - (pulp.lpSum(recruit[(k, j)] for j in range(i + 1)) + overmanning[(k, i)] - short[(k, i) / 2]) >= data['requirement'][k][i]), f"Manpower_Requirement_Constraint_{k}_{i}")

# Overmanning constraints
for i in range(I):
    problem += (pulp.lpSum(overmanning[(k, i)] for k in range(K)) <= data['num_overman']), f"Overmanning_Constraint_{i}"

# Solve the problem
problem.solve()

# Collecting the results
result = {
    "recruit": [[pulp.value(recruit[(k, i)]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[(k, i)]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[(k, i)]) for i in range(I)] for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')