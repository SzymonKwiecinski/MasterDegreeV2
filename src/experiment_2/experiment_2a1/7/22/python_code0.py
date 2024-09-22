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

K = len(data['strength'])
I = len(data['requirement'][0])

# Create the LP problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=lambda k, i: data['recruit'][k])
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, upBound=data['num_overman'])
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=data['num_shortwork'])

# Objective function: Minimize redundancy cost
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] + pulp.lpSum(recruit[k][i] for i in range(I)) - pulp.lpSum(overmanning[k][i] for i in range(I)) - pulp.lpSum(short[k][i] * 0.5 for i in range(I)) - sum(data['lessonewaste'][k] * data['strength'][k] for k in range(K)) - sum(data['moreonewaste'][k] * max(0, data['strength'][k] - data['lessonewaste'][k] * data['strength'][k]) for k in range(K))) for k in range(K))

# Constraints
for k in range(K):
    for i in range(I):
        problem += (pulp.lpSum(recruit[k][i] for i in range(I)) + data['strength'][k] - pulp.lpSum(overmanning[k][i] for i in range(I)) - pulp.lpSum(short[k][i] * 0.5 for i in range(I)) >= data['requirement'][k][i])

# Solve the problem
problem.solve()

# Extracting the results
results = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)],
}

print(json.dumps(results))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')