import pulp
import json

# Data in JSON format
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

# Create the problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
r = pulp.LpVariable.dicts("recruits", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
o = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("short_time_workers", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] * data['lessonewaste'][k] if i == 0 else 0) + 
                      data['costoverman'][k] * o[(k, i)] + 
                      data['costshort'][k] * s[(k, i)] 
                      for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - 
                     data['moreonewaste'][k] * data['strength'][k] - 
                     s[(k, i)] + 
                     r[(k, i)] + 
                     o[(k, i)] >= 
                     data['requirement'][k][i], f"Manpower_Balance_Constraint_{k}_{i}")

# Recruitment limit
for k in range(K):
    for i in range(I):
        problem += (r[(k, i)] <= data['recruit'][k], f"Recruitment_Limit_{k}_{i}")

# Overmanning constraint
for i in range(I):
    problem += (pulp.lpSum(o[(k, i)] for k in range(K)) <= data['num_overman'], f"Overmanning_Constraint_{i}")

# Short-time working constraint
for k in range(K):
    for i in range(I):
        problem += (s[(k, i)] <= data['num_shortwork'], f"Short_Work_Constraint_{k}_{i}")

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')