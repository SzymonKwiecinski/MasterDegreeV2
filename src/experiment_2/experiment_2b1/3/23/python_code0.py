import pulp
import json

# Input data as given in the DATA section
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

K = len(data['requirement'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the optimization problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit_vars = [[pulp.LpVariable(f'recruit_{k}_{i}', lowBound=0, upBound=data['recruit'][k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning_vars = [[pulp.LpVariable(f'overmanning_{k}_{i}', lowBound=0, cat='Integer') for i in range(I)] for k in range(K)]
short_vars = [[pulp.LpVariable(f'short_{k}_{i}', lowBound=0, upBound=data['num_shortwork'], cat='Integer') for i in range(I)] for k in range(K)]

# Objective function
costs = (
    sum(data['costredundancy'][k] * (data['strength'][k] - sum(recruit_vars[k]) - sum(overmanning_vars[k]) - sum(short_vars[k])) for k in range(K)) +
    sum(data['costoverman'][k] * overmanning_vars[k][i] for k in range(K) for i in range(I)) +
    sum(data['costshort'][k] * short_vars[k][i] for k in range(K) for i in range(I))
)
problem += costs

# Constraints
for i in range(I):
    for k in range(K):
        # Workforce balance considering wastage
        problem += (data['strength'][k] - sum(recruit_vars[k][i]) - sum(overmanning_vars[k][i]) - short_vars[k][i] * 0.5) >= data['requirement'][k][i]

# Overmanning constraint
for k in range(K):
    problem += sum(overmanning_vars[k][i] for i in range(I)) <= data['num_overman']

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)],
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')