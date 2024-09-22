import pulp
import json

# Data from the provided JSON
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
I = len(data['requirement'][0])

# Define the problem
problem = pulp.LpProblem("Minimize_Redundancy_Cost", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
redundancy_vars = pulp.LpVariable.dicts("redundancy", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')

# Objective Function
problem += pulp.lpSum(redundancy_vars[k][i] * data['costredundancy'][k] for k in range(K) for i in range(I))

# Constraints
strength_vars = [[0] * I for _ in range(K)]
for k in range(K):
    strength_vars[k][0] = data['strength'][k]  # Initial strength

for k in range(K):
    for i in range(1, I):
        strength_vars[k][i] = (strength_vars[k][i-1] + 
                                pulp.lpSum(recruit_vars[k][j] - redundancy_vars[k][j] for j in range(i+1)) - 
                                data['lessonewaste'][k] * recruit_vars[k][i] - 
                                data['moreonewaste'][k] * (strength_vars[k][i-1] - recruit_vars[k][i]))

# Manpower Balance & Requirement Satisfaction
for k in range(K):
    for i in range(I):
        problem += (strength_vars[k][i] + overmanning_vars[k][i] - short_vars[k][i] >= 
                     data['requirement'][k][i] + pulp.lpSum(short_vars[k][i]) / 2)

# Recruitment Limits
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k][i] <= data['recruit'][k]

# Overmanning and Short-time Limits
for i in range(I):
    problem += pulp.lpSum(overmanning_vars[k][i] for k in range(K)) <= data['num_overman']
    for k in range(K):
        problem += short_vars[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')