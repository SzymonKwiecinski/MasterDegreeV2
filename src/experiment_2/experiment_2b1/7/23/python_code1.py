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
K = len(data['strength'])  # number of manpower types
I = len(data['requirement'][0])  # number of years

# Create LP problem
problem = pulp.LpProblem("Minimize_Labor_Costs", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=500, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=50, cat='Integer')

# Objective Function
objective = pulp.lpSum(
    data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i] + short[k][i]*0.5) +
    data['costoverman'][k] * overmanning[k][i] +
    data['costshort'][k] * short[k][i]
    for k in range(K) for i in range(I)
)
problem += objective

# Constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - pulp.lpSum(recruit[k][j] for j in range(i + 1)) - overmanning[k][i] + short[k][i]*0.5 >= data['requirement'][k][i]), f"ManpowerRequirement_k{k}_i{i}"

# Overmanning constraint
problem += (pulp.lpSum(overmanning[k][i] for k in range(K) for i in range(I)) <= data['num_overman']), "TotalOvermanning"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

# Print results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')