import pulp
import json

# Data in JSON format
data_json = '''{
    "requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    "strength": [2000, 1500, 1000],
    "lessonewaste": [0.25, 0.2, 0.1],
    "moreonewaste": [0.1, 0.05, 0.05],
    "recruit": [500, 800, 500],
    "costredundancy": [200, 500, 500],
    "num_overman": 150,
    "costoverman": [1500, 2000, 3000],
    "num_shortwork": 50,
    "costshort": [500, 400, 400]
}'''

data = json.loads(data_json)

K = len(data['strength'])  # Number of categories
I = len(data['requirement'][0])  # Number of items

# Create problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("redundancy", (range(K), range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([
    data['costredundancy'][k] * redundancy[k][i] + 
    data['costoverman'][k] * overmanning[k][i] + 
    data['costshort'][k] * short[k][i] 
    for k in range(K) for i in range(I)
])

# Manpower Balance Constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            problem += (data['strength'][k] + recruit[k][0] - redundancy[k][0] >= 
                         data['requirement'][k][0] - short[k][0])
        else:
            problem += (recruit[k][i-1] * (1 - data['lessonewaste'][k]) + 
                         (data['strength'][k] + pulp.lpSum(recruit[k][m] * (1 - data['moreonewaste'][k]) for m in range(i))) - 
                         redundancy[k][i] >= 
                         data['requirement'][k][i] - short[k][i])

# Recruitment Limits
for k in range(K):
    for i in range(I):
        problem += recruit[k][i] <= data['recruit'][k]

# Overmanning Constraints
for i in range(I):
    problem += pulp.lpSum([overmanning[k][i] for k in range(K)]) <= data['num_overman']

# Short-time Constraints
for k in range(K):
    for i in range(I):
        problem += short[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')