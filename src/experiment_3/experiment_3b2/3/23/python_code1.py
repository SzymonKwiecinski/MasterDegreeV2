import pulp
import json

# Data provided in JSON format
data_str = "{'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}"
data = json.loads(data_str.replace("'", "\""))

# Parameters
K = len(data['requirement'])  # Number of categories
I = len(data['requirement'][0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=data['num_shortwork'])
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Initial Strength
strength = [[pulp.LpVariable(f'strength_{k}_{i}', lowBound=0) for i in range(I)] for k in range(K)]
for k in range(K):
    strength[k][0] = data['strength'][k]  # Initial strength

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * redundancy[k, i] + 
                       data['costoverman'][k] * overmanning[k, i] + 
                       data['costshort'][k] * short[k, i] 
                       for k in range(K) for i in range(I))

# Constraints
# Manpower Balance
for k in range(K):
    for i in range(1, I):
        problem += (strength[k][i] == strength[k][i-1] * (1 - data['moreonewaste'][k]) + 
                     recruit[k, i] * (1 - data['lessonewaste'][k]) - 
                     redundancy[k, i] + 
                     overmanning[k, i] + 
                     0.5 * short[k, i])

# Requirement Constraints
for k in range(K):
    for i in range(I):
        problem += (strength[k][i] >= data['requirement'][k][i])

# Recruitment Limits
for k in range(K):
    for i in range(I):
        problem += (recruit[k, i] <= data['recruit'][k])

# Overmanning Limits
for i in range(I):
    problem += (pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman'])

# Short-time Working Limits
for k in range(K):
    for i in range(I):
        problem += (short[k, i] <= data['num_shortwork'])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')