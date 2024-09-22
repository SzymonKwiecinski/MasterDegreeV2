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

# Problem setup
K = len(data['requirement'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=data['num_shortwork'], cat='Integer')

# Objective Function: Minimize total redundancy costs
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - pulp.lpSum(recruit[k][j] for j in range(I)) - pulp.lpSum(short[k][j] for j in range(I)) - pulp.lpSum(overmanning[k][j] for j in range(I)) - data['lessonewaste'][k] * data['strength'][k] - data['moreonewaste'][k] * (data['strength'][k] - data['requirement'][k][0])) for k in range(K))

# Constraints
for k in range(K):
    for i in range(I):
        # Total manpower available must meet the requirement
        problem += (data['strength'][k] + pulp.lpSum(recruit[k][j] for j in range(i + 1)) - pulp.lpSum(overmanning[k][i] for j in range(I)) - pulp.lpSum(short[k][j] for j in range(I))) >= data['requirement'][k][i]
        
# Maximum overmanning constraint
for k in range(K):
    problem += pulp.lpSum(overmanning[k][i] for i in range(I)) <= data['num_overman']

# Setting upper bounds for recruitment variables
for k in range(K):
    for i in range(I):
        recruit[k][i].upBound = data['recruit'][k]

# Solve the problem
problem.solve()

# Prepare the output
output_recruit = [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)]
output_overmanning = [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)]
output_short = [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]

output = {
    "recruit": output_recruit,
    "overmanning": output_overmanning,
    "short": output_short
}

# Print the results
print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')