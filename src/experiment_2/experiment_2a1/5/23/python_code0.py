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

# Define problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Parameters
K = len(data['requirement'])  # number of manpower types
I = len(data['requirement'][0])  # number of years

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective function
costs = (
    pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i]) for k in range(K) for i in range(I)) +
    pulp.lpSum(data['costoverman'][k] * overmanning[k][i] for k in range(K) for i in range(I)) +
    pulp.lpSum(data['costshort'][k] * short[k][i] for k in range(K) for i in range(I))
)
problem += costs

# Constraints
for i in range(I):
    for k in range(K):
        # manpower equation
        problem += (
            data['strength'][k] - 
            pulp.lpSum(recruit[k][i]) + 
            short[k][i] / 2 - 
            (data['strength'][k] * data['moreonewaste'][k]) >= data['requirement'][k][i]
        )

        # short-time working limit
        problem += short[k][i] <= data['num_shortwork']

        # overmanning limit
        problem += overmanning[k][i] <= data['num_overman']

# Solve problem
problem.solve()

# Output results
result = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')