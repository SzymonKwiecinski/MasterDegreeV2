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
    'costshort': [500, 400, 400],
}

K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Create the Linear Programming problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=data['recruit'][k])
overmanning_vars = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
short_vars = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=data['num_shortwork'])

# Objective Function
costs = []
for k in range(K):
    for i in range(I):
        costs.append((data['costredundancy'][k] * (data['strength'][k] + recruit_vars[(k, i)] - data['requirement'][k][i]) +
                       data['costoverman'][k] * pulp.lpSum(overmanning_vars[(k, i)]) +
                       data['costshort'][k] * short_vars[(k, i)]))

problem += pulp.lpSum(costs)

# Constraints
for k in range(K):
    for i in range(I):
        # Total manpower after accounting for wastage and short-term work
        problem += (data['strength'][k] * (1 - data['moreonewaste'][k]) + recruit_vars[(k, i)] -
                    short_vars[(k, i)] / 2 + overmanning_vars[(k, i)] >= data['requirement'][k][i])

# Overmanning constraint
for i in range(I):
    problem += pulp.lpSum(overmanning_vars[(k, i)] for k in range(K)) <= data['num_overman']

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "recruit": [[pulp.value(recruit_vars[(k, i)]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[(k, i)]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[(k, i)]) for i in range(I)] for k in range(K)],
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')