import pulp
import json

data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
redundant = pulp.LpVariable.dicts("redundant", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(
    data['costredundancy'][k] * redundant[k, i] +
    data['costoverman'][k] * overmanning[k, i] +
    data['costshort'][k] * short[k, i]
    for k in range(K) for i in range(I)
)

# Constraints
strength = pulp.LpVariable.dicts("strength", (k for k in range(K)), lowBound=0)

# Initial strength
for k in range(K):
    strength[k] = data['strength'][k] - data['moreonewaste'][k] * data['strength'][k] + \
                  recruit[k, 0] - redundant[k, 0]

# Strength balance constraints
for k in range(K):
    for i in range(1, I):
        problem += strength[k] == (1 - data['lessonewaste'][k]) * recruit[k, i - 1] + \
                   (1 - data['moreonewaste'][k]) * (strength[k] + overmanning[k, i - 1]) - redundant[k, i]

# Demand constraints
for k in range(K):
    for i in range(I):
        problem += strength[k] + overmanning[k, i] + 0.5 * short[k, i] >= data['requirement'][k][i]

# Recruitment constraints
for k in range(K):
    for i in range(I):
        problem += recruit[k, i] <= data['recruit'][k]

# Overmanning constraints
for i in range(I):
    problem += pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman']

# Short-time working constraints
for i in range(I):
    for k in range(K):
        problem += short[k, i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')