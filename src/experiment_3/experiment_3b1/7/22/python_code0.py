import pulp
import json

# Input data
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Parameters
K = len(data['strength'])  # Number of categories
I = len(data['requirement'][0])  # Number of years

# Create the problem variable
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * pulp.lpSum(pulp.max(0, data['strength'][k] - data['requirement'][k][i] + overmanning_vars[k][i]) for i in range(I)) for k in range(K))

# Constraints
# Constraint 1
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - (data['lessonewaste'][k] * recruit_vars[k][i] + data['moreonewaste'][k] * data['strength'][k]) + recruit_vars[k][i] - short_vars[k][i] + overmanning_vars[k][i] >= data['requirement'][k][i])

# Constraint 2
for i in range(I):
    problem += (pulp.lpSum(recruit_vars[k][i] for k in range(K)) <= data['num_overman'])

# Constraint 3
for k in range(K):
    for i in range(I):
        problem += (recruit_vars[k][i] <= data['recruit'][k])

# Constraint 4
for k in range(K):
    for i in range(I):
        problem += (overmanning_vars[k][i] <= data['num_overman'])

# Constraint 5
for k in range(K):
    for i in range(I):
        problem += (short_vars[k][i] <= data['num_shortwork'])

# Constraint 6
for k in range(K):
    for i in range(I):
        problem += (short_vars[k][i] <= 0.5 * (data['strength'][k] - data['requirement'][k][i]))

# Solve the problem
problem.solve()

# Output the results
recruit = [[recruit_vars[k][i].varValue for i in range(I)] for k in range(K)]
overmanning = [[overmanning_vars[k][i].varValue for i in range(I)] for k in range(K)]
short = [[short_vars[k][i].varValue for i in range(I)] for k in range(K)]

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')