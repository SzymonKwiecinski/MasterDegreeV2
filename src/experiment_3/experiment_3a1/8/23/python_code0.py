import pulp
import json

# Data from JSON format
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
K = len(data['strength'])
I = len(data['requirement'][0])

# Create the problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (k for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", (k for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", (k for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - 0.5 * short_vars[k, i] - overmanning_vars[k, i]) for k in range(K) for i in range(I)) \
                      + pulp.lpSum(data['costoverman'][k] * overmanning_vars[k, i] for k in range(K) for i in range(I)) \
                      + pulp.lpSum(data['costshort'][k] * short_vars[k, i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - data['lessonewaste'][k] * recruit_vars[k, i] - 
                     data['moreonewaste'][k] * data['strength'][k] + 
                     overmanning_vars[k, i] + 0.5 * short_vars[k, i] >= 
                     data['requirement'][k][i], f"Strength_Year_{k}_{i}")

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += (recruit_vars[k, i] <= data['recruit'][k], f"Recruit_Limit_{k}_{i}")

# Overmanning limits
problem += (pulp.lpSum(overmanning_vars[k, i] for k in range(K) for i in range(I)) <= data['num_overman'], "Overmanning_Limit")

# Short-time worker limits
for k in range(K):
    for i in range(I):
        problem += (short_vars[k, i] <= data['num_shortwork'], f"Short_Work_Limit_{k}_{i}")

# Solve the problem
problem.solve()

# Objective value output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')