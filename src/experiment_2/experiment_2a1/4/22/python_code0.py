import pulp
import json

# Input data
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

# Problem parameters
K = len(data['requirement'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), 0, None)
overmanning_vars = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), 0, None)
short_vars = pulp.LpVariable.dicts("Short", (range(K), range(I)), 0, None)
redundancy_vars = pulp.LpVariable.dicts("Redundancy", (range(K), range(I)), 0, None)

# Objective function: Minimize redundancy costs
problem += pulp.lpSum(data['costredundancy'][k] * redundancy_vars[k][i] for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    for k in range(K):
        problem += pulp.lpSum(recruit_vars[k][i] + overmanning_vars[k][i] + short_vars[k][i]) - (data['strength'][k] * (1 - data['moreonewaste'][k]) - data['requirement'][k][i]) <= data['num_overman']

        if i > 0:
            problem += (data['strength'][k] - pulp.lpSum(redundancy_vars[k][i]) - pulp.lpSum(recruit_vars[k][j] for j in range(i)) * (1 - data['lessonewaste'][k]) - short_vars[k][i] * 0.5) >= data['requirement'][k][i]

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k][i] <= data['recruit'][k]

# Short-time working limits
for k in range(K):
    for i in range(I):
        problem += short_vars[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Output results
recruit_result = [[[recruit_vars[k][i].varValue for i in range(I)] for k in range(K)]]
overmanning_result = [[[overmanning_vars[k][i].varValue for i in range(I)] for k in range(K)]]
short_result = [[[short_vars[k][i].varValue for i in range(I)] for k in range(K)]]

output = {
    "recruit": recruit_result,
    "overmanning": overmanning_result,
    "short": short_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')