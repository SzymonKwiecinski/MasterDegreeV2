import pulp
import json

data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

K = len(data['strength'])
I = len(data['requirement'][0])

# Create the LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
redundant = pulp.LpVariable.dicts("redundant", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
total = pulp.LpVariable.dicts("total", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * redundant[k, i] + 
                       data['costoverman'][k] * overmanning[k, i] + 
                       data['costshort'][k] * short[k, i]
                       for k in range(K) for i in range(I))

# Constraints
# Initial Condition
problem += (total[0, 0] == data['strength'][0])
for k in range(1, K):
    problem += (total[k, 0] == data['strength'][k])

# Manpower Balance
for i in range(1, I):
    for k in range(K):
        problem += (total[k, i] == (1 - data['moreonewaste'][k]) * total[k, i-1] + 
                     recruit[k, i] - redundant[k, i] + overmanning[k, i])

# Short-time Working Limit
for i in range(I):
    for k in range(K):
        problem += (short[k, i] <= data['num_shortwork'])

# Service Requirements
for i in range(I):
    for k in range(K):
        problem += (data['requirement'][k][i] <= total[k, i] + 0.5 * short[k, i])

# Recruitment Limits
for i in range(I):
    for k in range(K):
        problem += (recruit[k, i] <= data['recruit'][k])

# Overmanning Limits
for i in range(I):
    problem += (pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman'])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')