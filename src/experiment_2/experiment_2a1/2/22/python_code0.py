import pulp
import json

data = {'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
        'strength': [2000, 1500, 1000], 
        'lessonewaste': [0.25, 0.2, 0.1], 
        'moreonewaste': [0.1, 0.05, 0.05], 
        'recruit': [500, 800, 500], 
        'costredundancy': [200, 500, 500], 
        'num_overman': 150, 
        'costoverman': [1500, 2000, 3000], 
        'num_shortwork': 50, 
        'costshort': [500, 400, 400]}

K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective function: minimize redundancy cost
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - pulp.lpSum(recruit[k][i] + short[k][i] / 2 + overmanning[k][i] for i in range(I)) ) for k in range(K))

# Constraints
for i in range(I):
    for k in range(K):
        # Wastage due to less than and more than one year service
        current_strength = data['strength'][k] * (1 - data['lessonewaste'][k]) * (1 - data['moreonewaste'][k])
        
        problem += (current_strength + recruit[k][i] + short[k][i] - overmanning[k][i] >= data['requirement'][k][i])

        # Limit on recruitment
        problem += pulp.lpSum(recruit[k][i] for k in range(K)) <= data['recruit'][k]

        # Limit on overmanning
        problem += pulp.lpSum(overmanning[k][i] for k in range(K)) <= data['num_overman']

        # Limit on short-time work
        problem += pulp.lpSum(short[k][i] for k in range(K)) <= data['num_shortwork']

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')