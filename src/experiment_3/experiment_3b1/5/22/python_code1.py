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

# Indices
K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Create a linear programming problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * 
                      (data['strength'][k] - data['requirement'][k][i] + 
                       overmanning_vars[k, i] - short_vars[k, i] / 2.0)  # fixed division to float
                      for k in range(K) for i in range(I))

# Constraints
# Recruitment limit
for k in range(K):
    problem += pulp.lpSum(recruit_vars[k, i] for i in range(I)) <= data['recruit'][k]

# Overmanning limit
for k in range(K):
    problem += pulp.lpSum(overmanning_vars[k, i] for i in range(I)) <= data['num_overman']

# Short-time working limit
for k in range(K):
    problem += pulp.lpSum(short_vars[k, i] for i in range(I)) <= data['num_shortwork']

# Manpower balance equation
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - (data['lessonewaste'][k] * data['strength'][k]) - 
                    (data['moreonewaste'][k] * (data['strength'][k] - pulp.lpSum(recruit_vars[k, j] for j in range(i + 1)))) == 
                    data['requirement'][k][i] + overmanning_vars[k, i] - short_vars[k, i] / 2.0)  # fixed division to float

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')