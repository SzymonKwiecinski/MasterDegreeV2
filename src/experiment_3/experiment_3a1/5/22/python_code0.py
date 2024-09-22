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

I = len(data['requirement'])  # Number of years
K = len(data['requirement'][0])  # Number of manpower categories

# Create the problem variable
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
redundancy = {}
for k in range(K):
    for i in range(I):
        redundancy[(k, i)] = pulp.LpVariable(f"redundancy_{k}_{i}", lowBound=0, cat='Continuous')
        problem += redundancy[(k, i)] == pulp.lpSum([
            data['strength'][k] - 
            (1 - data['moreonewaste'][k]) * data['strength'][k] - 
            recruit_vars[(k, i)] - 
            overmanning_vars[(k, i)] + 
            short_vars[(k, i)]
        ])

problem += pulp.lpSum(data['costredundancy'][k] * redundancy[(k, i)] for k in range(K) for i in range(I))

# Constraints
# Manpower Requirement
for i in range(I):
    problem += pulp.lpSum([
        data['strength'][k] - 
        data['lessonewaste'][k] * data['strength'][k] - 
        data['moreonewaste'][k] * (1 - data['lessonewaste'][k]) * data['strength'][k] + 
        recruit_vars[(k, i)] + 
        overmanning_vars[(k, i)] - 
        short_vars[(k, i)]
        for k in range(K)
    ]) >= pulp.lpSum(data['requirement'][i][k] for k in range(K))

# Overmanning Limit
for i in range(I):
    problem += pulp.lpSum(overmanning_vars[(k, i)] for k in range(K)) <= data['num_overman']

# Short-Time Working Limit
for k in range(K):
    for i in range(I):
        problem += short_vars[(k, i)] <= data['num_shortwork']

# Recruitment Limit
for k in range(K):
    for i in range(I):
        problem += recruit_vars[(k, i)] <= data['recruit'][k]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')