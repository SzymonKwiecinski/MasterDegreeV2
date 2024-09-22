import json
import pulp

# Input JSON data
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

# Extract data
requirements = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limit = data['recruit']
cost_redundancy = data['costredundancy']
num_overman = data['num_overman']
cost_overman = data['costoverman']
num_shortwork = data['num_shortwork']
cost_short = data['costshort']

# Define the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Define indices
K = len(requirements)  # Number of manpower types
I = len(requirements[0])  # Number of years

# Decision variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overman_vars = pulp.LpVariable.dicts("overman", (range(K), range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective function
total_cost = (
    pulp.lpSum(cost_redundancy[k] * (strength[k] - requirements[k][i]) for k in range(K) for i in range(I) if strength[k] > requirements[k][i]) +
    pulp.lpSum(cost_overman[k] * overman_vars[k][i] for k in range(K) for i in range(I)) +
    pulp.lpSum(cost_short[k] * short_vars[k][i] for k in range(K) for i in range(I))
)
problem += total_cost

# Constraints
for i in range(I):
    for k in range(K):
        # Total manpower after adjustments must meet requirements
        problem += (strength[k] + pulp.lpSum(recruit_vars[k][j] for j in range(i + 1)) - 
                     pulp.lpSum(short_vars[k][j] for j in range(i + 1)) - 
                     pulp.lpSum(overman_vars[k][j] for j in range(i + 1)) >= requirements[k][i])

# Recruiting constraints
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k][i] <= recruit_limit[k]

# Overman constraints
for k in range(K):
    for i in range(I):
        problem += overman_vars[k][i] <= num_overman

# Short work constraints
for k in range(K):
    for i in range(I):
        problem += short_vars[k][i] <= num_shortwork

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overman_vars[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result
print(json.dumps(output, indent=4))