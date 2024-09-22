import pulp
import json

# Data provided in JSON format
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
I = len(data['requirement'])

# Create the linear programming problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=800) 
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0) 
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=50) 

# Redundant variable for each category and year (assuming redundant is the same as overmanning in the context)
redundant = pulp.LpVariable.dicts("redundant", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * redundant[k, i] +
                       data['costoverman'][k] * overmanning[k, i] +
                       data['costshort'][k] * short[k, i] 
                       for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    for k in range(K):
        problem += (data['strength'][k] - 
                     (1 - data['moreonewaste'][k]) * (data['strength'][k] - redundant[k, i]) + 
                     recruit[k, i] + 
                     overmanning[k, i] + 
                     short[k, i] / 2 >= data['requirement'][k][i])

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += recruit[k, i] <= data['recruit'][k]

# Redundancy management
for k in range(K):
    for i in range(I):
        problem += redundant[k, i] >= 0

# Overmanning restrictions
for i in range(I):
    problem += pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman']

# Short-time working limits
for k in range(K):
    for i in range(I):
        problem += short[k, i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')