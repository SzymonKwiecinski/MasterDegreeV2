import pulp
import json

# Given data
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
K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), 0, None, pulp.LpInteger)
overmanning_vars = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), 0, None, pulp.LpInteger)
short_vars = pulp.LpVariable.dicts("Short", (range(K), range(I)), 0, None, pulp.LpInteger)

# Objective Function: Minimize costs
costs = (
    pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] + pulp.lpSum(recruit_vars[k][i] for i in range(I)) - data['requirement'][k][i] - overmanning_vars[k][i] + short_vars[k][i] * 0.5) for k in range(K) for i in range(I))
    + pulp.lpSum(data['costoverman'][k] * overmanning_vars[k][i] for k in range(K) for i in range(I))
    + pulp.lpSum(data['costshort'][k] * short_vars[k][i] for k in range(K) for i in range(I))
)

problem += costs

# Constraints
for k in range(K):
    for i in range(I):
        problem += (
            data['strength'][k] * (1 - data['moreonewaste'][k]) + pulp.lpSum(recruit_vars[k][j] for j in range(i + 1)) - pulp.lpSum(overmanning_vars[k][j] for j in range(I)) + 0.5 * pulp.lpSum(short_vars[k][j] for j in range(I)) >= data['requirement'][k][i],
            f"ManpowerRequirement_{k}_{i}"
        )

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k][i] <= data['recruit'][k], f"RecruitLimit_{k}_{i}"

# Overmanning limit
for i in range(I):
    problem += pulp.lpSum(overmanning_vars[k][i] for k in range(K)) <= data['num_overman'], f"OvermanningLimit_{i}"

# Short-time working limit
for k in range(K):
    for i in range(I):
        problem += short_vars[k][i] <= data['num_shortwork'], f"ShortWorkLimit_{k}_{i}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[int(recruit_vars[k][i].varValue) for i in range(I)] for k in range(K)],
    "overmanning": [[int(overmanning_vars[k][i].varValue) for i in range(I)] for k in range(K)],
    "short": [[int(short_vars[k][i].varValue) for i in range(I)] for k in range(K)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the output
print(output)