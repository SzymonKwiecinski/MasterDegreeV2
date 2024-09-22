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

# Constants
K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')

# Objective function: Minimize costs
total_cost = pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i] + overmanning_vars[(k, i)] - short_vars[(k,i)]) for k in range(K) for i in range(I)) \
              + pulp.lpSum(data['costoverman'][k] * overmanning_vars[(k, i)] for k in range(K) for i in range(I)) \
              + pulp.lpSum(data['costshort'][k] * short_vars[(k, i)] for k in range(K) for i in range(I))
              
problem += total_cost

# Constraints

# Manpower requirement constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] * (1 - data['moreonewaste'][k]) + recruit_vars[(k, i)] - short_vars[(k, i)] >= data['requirement'][k][i])
        
# Recruitment limits
for k in range(K):
    problem += pulp.lpSum(recruit_vars[(k, i)] for i in range(I)) <= data['recruit'][k]

# Overmanning constraints
for i in range(I):
    problem += pulp.lpSum(overmanning_vars[(k, i)] for k in range(K)) <= data['num_overman']

# Short-time working constraints
for k in range(K):
    for i in range(I):
        problem += short_vars[(k, i)] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit_vars[(k, i)]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[(k, i)]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[(k, i)]) for i in range(I)] for k in range(K)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')