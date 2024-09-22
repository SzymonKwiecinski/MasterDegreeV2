import pulp
import json

# Data input
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

# Parameters
K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, upBound=data['num_shortwork'], cat='Integer')

# Objective function
costs = pulp.lpSum(recruit[k][i] * data['costredundancy'][k] for k in range(K) for i in range(I)) + \
        pulp.lpSum(overmanning[k][i] * data['costoverman'][k] for k in range(K) for i in range(I)) + \
        pulp.lpSum(short[k][i] * data['costshort'][k] for k in range(K) for i in range(I))

problem += costs, "Total_Cost"

# Constraints
for i in range(I):
    for k in range(K):
        current_strength = data['strength'][k] * (1 - data['moreonewaste'][k]) if i > 0 else data['strength'][k] * (1 - data['lessonewaste'][k])
        problem += (current_strength + pulp.lpSum(recruit[k][j] for j in range(i + 1)) +
                     pulp.lpSum(overmanning[k][j] for j in range(i + 1)) - 
                     pulp.lpSum(short[k][j] for j in range(i + 1))) >= data['requirement'][k][i], f"Manpower_Requirement_Constraint_{k}_{i}"

# Overmanning constraint
for i in range(I):
    problem += pulp.lpSum(overmanning[k][i] for k in range(K)) <= data['num_overman'], f"Overmanning_Constraint_{i}"

# Recruit upper bounds correction
for k in range(K):
    for i in range(I):
        recruit[k][i].upBound = data['recruit'][k]

# Solve the problem
problem.solve()

# Extract results
recruit_result = [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)]
overmanning_result = [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)]
short_result = [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]

# Output results
output = {
    "recruit": recruit_result,
    "overmanning": overmanning_result,
    "short": short_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')