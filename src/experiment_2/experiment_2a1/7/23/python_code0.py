import pulp
import json

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

K = len(data['strength'])  # number of manpower types
I = len(data['requirement'][0])  # number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function: Minimize costs
costs = (
    pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i] + overmanning_vars[(k, i)]) for k in range(K) for i in range(I) if data['strength'][k] > data['requirement'][k][i]) +
    pulp.lpSum(data['costshort'][k] * short_vars[(k, i)] for k in range(K) for i in range(I)) +
    pulp.lpSum(data['costoverman'][k] * overmanning_vars[(k, i)] for k in range(K) for i in range(I)) +
    pulp.lpSum(data['costshort'][k] * short_vars[(k, i)] for k in range(K) for i in range(I))
)
problem += costs

# Constraints
for i in range(I):
    for k in range(K):
        problem += (data['strength'][k] - 
                     sum(recruit_vars[(k, j)] for j in range(i + 1)) * (1 - data['lessonewaste'][k]) -
                     data['requirement'][k][i] +
                     sum(short_vars[(k, j)] for j in range(I)) / 2 +
                     overmanning_vars[(k, i)] <= 0, f"Manpower_Requirement_k{k}_i{i}")

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += (recruit_vars[(k, i)] <= data['recruit'][k], f"Recruitment_Limit_k{k}_i{i}")

# Overmanning limit
for i in range(I):
    problem += (pulp.lpSum(overmanning_vars[(k, i)] for k in range(K)) <= data['num_overman'], f"Overmanning_Limit_i{i}")

# Short-time working limit
for k in range(K):
    for i in range(I):
        problem += (short_vars[(k, i)] <= data['num_shortwork'], f"Short_Work_Limit_k{k}_i{i}")

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit_vars[(k, i)]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[(k, i)]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[(k, i)]) for i in range(I)] for k in range(K)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')