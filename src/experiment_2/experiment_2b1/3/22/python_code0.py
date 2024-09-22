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

# Model
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Constants
K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Decision variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=data['recruit'], cat='Integer')
overman_vars = pulp.LpVariable.dicts("Overman", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=data['num_shortwork'], cat='Integer')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - sum(recruit_vars[k, i] for i in range(I)) - sum(overman_vars[k, i] for i in range(I)) + sum(short_vars[k, i] for i in range(I)) - data['requirement'][k][i] for k in range(K) for i in range(I))), "Total Redundancy Cost"

# Constraints
# Total manpower after recruitment, overmanning and short work
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - pulp.lpSum(recruit_vars[k, j] for j in range(I)) - pulp.lpSum(overman_vars[k, j] for j in range(I)) + pulp.lpSum(short_vars[k, j] for j in range(I))) >= data['requirement'][k][i] - (data['num_overman'] if k == 0 else 0), f"Manpower_Constraint_k_{k}_i_{i}"

# Solve the problem
problem.solve()

# Output result
recruit_result = [[[pulp.value(recruit_vars[k, i]) for i in range(I)] for k in range(K)]]
overmanning_result = [[[pulp.value(overman_vars[k, i]) for i in range(I)] for k in range(K)]]
short_result = [[[pulp.value(short_vars[k, i]) for i in range(I)] for k in range(K)]]

output = {
    "recruit": recruit_result,
    "overmanning": overmanning_result,
    "short": short_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')