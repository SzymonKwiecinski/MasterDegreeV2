import pulp
import json

# Data from the JSON format
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

# Create the problem variable
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
redundancy_vars = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * redundancy_vars[(k, i)] for k in range(K) for i in range(I))

# Constraints
# Manpower balance constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] 
                     - redundancy_vars[(k, i)] 
                     + recruit_vars[(k, i)] 
                     - data['lessonewaste'][k] * data['strength'][k]
                     - 0.5 * short_vars[(k, i)] 
                     >= data['requirement'][k][i])

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += recruit_vars[(k, i)] <= data['recruit'][k]

# Overmanning limits
for i in range(I):
    problem += pulp.lpSum(overmanning_vars[(k, i)] for k in range(K)) <= data['num_overman']

# Short-time working limits
for k in range(K):
    for i in range(I):
        problem += short_vars[(k, i)] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')