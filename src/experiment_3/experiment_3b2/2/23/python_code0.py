import pulp
import json

# Data from JSON
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
I = len(data['requirement'])  # Number of years

# Initialize the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
recruitment = pulp.LpVariable.dicts("recruitment", (range(K), range(I)), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("redundancy", (range(K), range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, 
                                     upBound=data['num_overman'], cat='Continuous')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, 
                               upBound=data['num_shortwork'], cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * redundancy[k][i] +
                       data['costoverman'][k] * overmanning[k][i] +
                       data['costshort'][k] * short[k][i]
                       for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        available_manpower = (data['strength'][k] + recruitment[k][i] + 
                              data['moreonewaste'][k] * 
                              (data['strength'][k] + 
                               pulp.lpSum(recruitment[k][j] * (1 - data['lessonewaste'][k] ) 
                                          for j in range(i))))
        
        problem += (available_manpower - redundancy[k][i] + 
                     overmanning[k][i] + 0.5 * short[k][i] >= 
                     data['requirement'][i][k])

# Recruitment constraints
for k in range(K):
    for i in range(I):
        problem += recruitment[k][i] <= data['recruit'][k]

# Redundancy constraints
for k in range(K):
    for i in range(I):
        problem += redundancy[k][i] >= 0

# Overmanning constraints
for k in range(K):
    for i in range(I):
        problem += overmanning[k][i] <= data['num_overman']

# Short constraints
for k in range(K):
    for i in range(I):
        problem += short[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')