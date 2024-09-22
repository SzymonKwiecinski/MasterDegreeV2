import pulp
import json

# Data input (normally this would be read from a file, here it's hardcoded for the example)
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Constants
K = len(data['strength'])
I = len(data['requirement'])

# Create the problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=lambda k: data['recruit'][k])
overmanning = pulp.LpVariable.dicts("overmanning", (k for k in range(K)), lowBound=0)
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=data['num_shortwork'])

# Redundancy calculations as a function
def calculate_redundancy(k, i):
    return pulp.lpSum([
        (data['strength'][k] - data['lessonewaste'][k] * recruit[(k, i)] - overmanning[k] - short[(k, i)] / 2 - data['requirement'][k][i]),
        0
    ])

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * calculate_redundancy(k, i) for k in range(K) for i in range(I))

# Constraints
# Recruitment Constraint
for k in range(K):
    for i in range(I):
        problem += recruit[(k, i)] <= data['recruit'][k]

# Overmanning Constraint
for i in range(I):
    problem += pulp.lpSum(overmanning[k] for k in range(K)) <= data['num_overman']

# Short-time Working Constraint
for k in range(K):
    for i in range(I):
        problem += short[(k, i)] <= data['num_shortwork']

# Non-negativity Constraints (handled by variable bounds)

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')