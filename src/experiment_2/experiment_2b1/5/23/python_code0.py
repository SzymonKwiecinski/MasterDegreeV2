import pulp
import json

# Input data in JSON format
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

# Define number of manpower types and years
K = len(data['strength'])
I = len(data['requirement'][0])

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=500, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=50, cat='Integer')

# Objective function
costs = (
    pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i]) for k in range(K) for i in range(I) if (data['strength'][k] - data['requirement'][k][i]) < 0) +
    pulp.lpSum(data['costoverman'][k] * overmanning_vars[k][i] for k in range(K) for i in range(I)) +
    pulp.lpSum(data['costshort'][k] * short_vars[k][i] for k in range(K) for i in range(I))
)

problem += costs

# Constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] + pulp.lpSum(recruit_vars[k][j] for j in range(i + 1)) + overmanning_vars[k][i] - short_vars[k][i] >= data['requirement'][k][i])
        
problem += (pulp.lpSum(overmanning_vars[k][i] for k in range(K) for i in range(I)) <= data['num_overman'])

# Solve the problem
problem.solve()

# Prepare the output
recruit_output = [[recruit_vars[k][i].varValue for i in range(I)] for k in range(K)]
overmanning_output = [[overmanning_vars[k][i].varValue for i in range(I)] for k in range(K)]
short_output = [[short_vars[k][i].varValue for i in range(I)] for k in range(K)]

output = {
    "recruit": recruit_output,
    "overmanning": overmanning_output,
    "short": short_output
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')