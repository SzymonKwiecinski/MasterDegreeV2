import pulp
import json

# Load data
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Define indices for manpower types and years
K = len(data['strength'])
I = len(data['requirement'][0])

# Create the problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("overman", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
z = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (
    data['strength'][k] + x[k, i] - (data['lessonewaste'][k] * (x[k, i] + data['strength'][k]) + data['moreonewaste'][k] * data['strength'][k]) - data['requirement'][k][i] + y[k, i] + z[k, i]) 
    + data['costoverman'][k] * y[k, i] + data['costshort'][k] * z[k, i]
    for k in range(K) for i in range(I))

# Constraints
# 1. Manpower balance
for k in range(K):
    for i in range(I):
        waste = data['lessonewaste'][k] * (x[k, i] + data['strength'][k]) + data['moreonewaste'][k] * data['strength'][k]
        problem += data['strength'][k] + x[k, i] - waste + y[k, i] + z[k, i] >= data['requirement'][k][i]

# 2. Recruitment limits
for k in range(K):
    for i in range(I):
        problem += x[k, i] <= data['recruit'][k]

# 3. Overmanning limits
for i in range(I):
    problem += pulp.lpSum(y[k, i] for k in range(K)) <= data['num_overman']

# 4. Short-time working limits
for k in range(K):
    for i in range(I):
        problem += z[k, i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Extract and print results
recruit_plan = [[pulp.value(x[k, i]) for i in range(I)] for k in range(K)]
overmanning_plan = [[pulp.value(y[k, i]) for i in range(I)] for k in range(K)]
short_plan = [[pulp.value(z[k, i]) for i in range(I)] for k in range(K)]

result = {
    "recruit": recruit_plan,
    "overmanning": overmanning_plan,
    "short": short_plan
}

print(f'Result: {json.dumps(result, indent=4)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')