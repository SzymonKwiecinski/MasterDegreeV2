import pulp
import json

# Data from JSON format
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

K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create a linear programming problem
problem = pulp.LpProblem("ManpowerManagement", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0)
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0)
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * pulp.lpMax(0, data['strength'][k] - data['requirement'][k][i]) + 
                      data['costoverman'][k] * overmanning[k][i] + 
                      data['costshort'][k] * short[k][i] 
                      for k in range(K) for i in range(I))

# Constraints
# Manpower Requirement Constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] + recruit[k][i] - 
                     data['moreonewaste'][k] * (data['strength'][k] - short[k][i]) >= 
                     data['requirement'][k][i] - overmanning[k][i])

# Recruitment Constraints
for k in range(K):
    for i in range(I):
        problem += recruit[k][i] <= data['recruit'][k]

# Overmanning Constraints
for i in range(I):
    problem += pulp.lpSum(overmanning[k][i] for k in range(K)) <= data['num_overman']

# Short-time Working Constraints
for k in range(K):
    for i in range(I):
        problem += short[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')