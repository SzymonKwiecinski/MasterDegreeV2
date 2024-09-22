import pulp
import json

# Data input
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

# Constants
K = len(data['strength'])  # number of manpower types
I = len(data['requirement'][0])  # number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=500, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=50, cat='Integer')

# Objective function: Minimize redundancy costs
problem += pulp.lpSum(data['costredundancy'][k] * 
                      (data['strength'][k] - 
                       (pulp.lpSum(data['requirement'][k][i] - (short[k][i] / 2) - overmanning[k][i] 
                       for i in range(I)))) 
                      for k in range(K))

# Constraints
for i in range(I):
    for k in range(K):
        # Total manpower available should meet or exceed requirements
        problem += (data['strength'][k] + 
                     pulp.lpSum(recruit[k][i]) - 
                     pulp.lpSum(overmanning[k][i]) - 
                     short[k][i] >= data['requirement'][k][i]), f"Manpower_Requirement_{k}_{i}"

# Limits on overmanning
for k in range(K):
    problem += pulp.lpSum(overmanning[k][i] for i in range(I)) <= data['num_overman'], f"Overmanning_Limit_{k}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')