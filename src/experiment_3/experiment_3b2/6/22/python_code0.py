import pulp
import json

# Data input
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Constants
K = len(data['requirement'])  # Number of skill categories
I = len(data['requirement'][0])  # Number of years considered

# Problem Definition
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * recruit_vars[k][i] for k in range(K) for i in range(I))

# Constraints
strength = [[data['strength'][k] for k in range(K)]]
for year in range(I):  
    for k in range(K):
        if year > 0:  # For i=0, we don't have a previous year's strength
            strength[k].append((1 - data['moreonewaste'][k]) * 
                                (strength[k][year - 1] + recruit_vars[k][year - 1]) + 
                                overmanning_vars[k][year] + 
                                0.5 * short_vars[k][year])
        else:
            strength[k].append(strength[k][0])  # Use initial strength for first year

# Manpower balance constraint
for k in range(K):
    for i in range(1, I):
        problem += strength[k][i] == (1 - data['moreonewaste'][k]) * (
            strength[k][i - 1] + recruit_vars[k][i - 1]) + overmanning_vars[k][i] + 0.5 * short_vars[k][i]

# Requirement satisfaction
for k in range(K):
    for i in range(I):
        problem += strength[k][i] >= data['requirement'][k][i]

# Recruitment limit
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k][i] <= data['recruit'][k]

# Overmanning constraint
for i in range(I):
    problem += pulp.lpSum(overmanning_vars[k][i] for k in range(K)) <= data['num_overman']

# Short-time working constraint
for k in range(K):
    for i in range(I):
        problem += short_vars[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')