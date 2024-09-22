import pulp
import json

# Input data
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

# Parameters
K = len(data['strength'])  # Number of skill levels
I = len(data['requirement'][0])  # Number of years
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

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=recruit)
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0)
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=num_shortwork)

# Objective function: minimize costs
total_cost = pulp.lpSum([costredundancy[k] * (strength[k] + pulp.lpSum(recruit_vars[k][i] for i in range(I)) - requirement[k][i] - overmanning_vars[k][i] - (short_vars[k][i] / 2)) for k in range(K) for i in range(I)]) + \
                         pulp.lpSum([costoverman[k] * overmanning_vars[k][i] for k in range(K) for i in range(I)]) + \
                         pulp.lpSum([costshort[k] * short_vars[k][i] for k in range(K) for i in range(I)])
problem += total_cost

# Constraints
for k in range(K):
    for i in range(I):
        # Balance equation
        problem += (strength[k] + pulp.lpSum(recruit_vars[k][j] for j in range(i + 1)) - \
                     pulp.lpSum(overmanning_vars[k][j] for j in range(i + 1)) - \
                     pulp.lpSum(short_vars[k][j] for j in range(i + 1)) - \
                     (strength[k] * (1 - lessonewaste[k]) if i == 0 else strength[k] * (1 - moreonewaste[k])) >= requirement[k][i], f"Balance_Constraint_{k}_{i}")

# Overmanning constraint
for i in range(I):
    problem += (pulp.lpSum(overmanning_vars[k][i] for k in range(K)) <= num_overman, f"Overmanning_Constraint_{i}")

# Solve the problem
problem.solve()

# Output the results
output = {
    "recruit": [[recruit_vars[k][i].varValue for i in range(I)] for k in range(K)],
    "overmanning": [[overmanning_vars[k][i].varValue for i in range(I)] for k in range(K)],
    "short": [[short_vars[k][i].varValue for i in range(I)] for k in range(K)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')