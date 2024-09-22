import pulp
import json

# Input Data
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

# Extracting parameters from the data
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(requirement)  # Number of categories
I = len(requirement[0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (k for k in range(K) for i in range(I)), lowBound=0, upBound=500)
overmanning_vars = pulp.LpVariable.dicts("overmanning", (k for k in range(K) for i in range(I)), lowBound=0)
short_vars = pulp.LpVariable.dicts("short", (k for k in range(K) for i in range(I)), lowBound=0)

# Objective Function
total_cost = pulp.lpSum([costredundancy[k] * recruit_vars[k, i] for k in range(K) for i in range(I)]) + \
             pulp.lpSum([costoverman[k] * overmanning_vars[k, i] for k in range(K) for i in range(I)]) + \
             pulp.lpSum([costshort[k] * short_vars[k, i] for k in range(K) for i in range(I)])

problem += total_cost

# Constraints
for k in range(K):
    for i in range(I):
        problem += (strength[k] * (1 - lessonewaste[k]) * (i == 0) + 
                     strength[k] * (1 - moreonewaste[k]) * (i > 0) + \
                     recruit_vars[k, i] + \
                     overmanning_vars[k, i] >= requirement[k][i] + short_vars[k, i] / 2, 
                     f"manpower_req_{k}_{i}")

# Overmanning constraint
for i in range(I):
    problem += pulp.lpSum([overmanning_vars[k, i] for k in range(K)]) <= num_overman, f"overmanning_limit_{i}"

# Short-time working constraint
for k in range(K):
    for i in range(I):
        problem += short_vars[k, i] <= num_shortwork, f"short_time_limit_{k}_{i}"

# Solve the problem
problem.solve()

# Prepare output data
output = {
    "recruit": [[recruit_vars[k, i].varValue for i in range(I)] for k in range(K)],
    "overmanning": [[overmanning_vars[k, i].varValue for i in range(I)] for k in range(K)],
    "short": [[short_vars[k, i].varValue for i in range(I)] for k in range(K)]
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')