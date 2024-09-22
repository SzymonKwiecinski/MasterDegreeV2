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

# Defining the problem
K = len(data['strength'])  # number of manpower types
I = len(data['requirement'][0])  # number of years

problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
r = pulp.LpVariable.dicts("r", (range(K), range(I)), lowBound=0, cat='Continuous')  # Recruits
o = pulp.LpVariable.dicts("o", (range(K), range(I)), lowBound=0, cat='Continuous')  # Overmanned workers
s = pulp.LpVariable.dicts("s", (range(K), range(I)), lowBound=0, cat='Continuous')  # Short-time workers

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i] - o[k][i] - 0.5 * s[k][i])
                      + data['costoverman'][k] * o[k][i]
                      + data['costshort'][k] * s[k][i]
                      for k in range(K) for i in range(I))

# Constraints

# Manpower Requirement
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - 
                     pulp.lpSum(data['lessonewaste'][k] * r[k][j] for j in range(i + 1)) -
                     pulp.lpSum(data['moreonewaste'][k] * (data['strength'][k] - pulp.lpSum(r[k][j] for j in range(i + 1))) for j in range(i + 1)) -
                     o[k][i] - 0.5 * s[k][i] >= data['requirement'][k][i])

# Recruitment Limit
for k in range(K):
    for i in range(I):
        problem += r[k][i] <= data['recruit'][k]

# Overmanning Limit
problem += pulp.lpSum(o[k][i] for k in range(K) for i in range(I)) <= data['num_overman']

# Short-time Working Limit
for k in range(K):
    for i in range(I):
        problem += s[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')