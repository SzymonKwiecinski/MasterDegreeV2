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

# Load the data
data = json.loads(data_json)

# Extract data
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(strength)
I = len(requirement[0])

# Create the problem
problem = pulp.LpProblem("Workforce_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
y = pulp.LpVariable.dicts("y", (k for k in range(K) for i in range(I)), lowBound=0)
z = pulp.LpVariable.dicts("z", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
r = pulp.LpVariable.dicts("r", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective function
problem += pulp.lpSum(costredundancy[k] * r[k, i] + costoverman[k] * y[k, i] + costshort[k] * z[k, i] for k in range(K) for i in range(I))

# Current workforce balance constraints
for k in range(K):
    problem += (pulp.lpSum(strength[k] + x[k, 0] - r[k, 0] - lessonewaste[k] * x[k, 0]) == requirement[k][0] + y[k, 0] - z[k, 0] / 2)

# Workforce balance for subsequent years
for i in range(1, I):
    for k in range(K):
        problem += (pulp.lpSum(strength[k] + x[k, i] - r[k, i] - moreonewaste[k] * (strength[k] + x[k, i-1] - lessonewaste[k] * x[k, i-1])) == requirement[k][i] + y[k, i] - z[k, i] / 2)

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += x[k, i] <= recruit[k]

# Overmanning limit
for i in range(I):
    problem += pulp.lpSum(y[k, i] for k in range(K)) <= num_overman

# Short-time working limits
for k in range(K):
    for i in range(I):
        problem += z[k, i] <= num_shortwork

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')