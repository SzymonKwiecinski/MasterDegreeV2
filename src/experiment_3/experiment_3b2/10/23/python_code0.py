import pulp
import json

# Load the data from the provided JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Define parameters
K = len(data['requirement'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the problem variable
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("redundancy", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * redundancy[k][i] +
                       data['costoverman'][k] * overmanning[k][i] +
                       data['costshort'][k] * short[k][i]
                       for k in range(K) for i in range(I))

# Constraints

# Manpower Balance
for k in range(K):
    for i in range(I):
        requirement = data['requirement'][k][i]
        strength = data['strength'][k]
        moreonewaste = data['moreonewaste'][k]
        problem += (strength - (moreonewaste * strength) + recruit[k][i] - redundancy[k][i] +
                     overmanning[k][i] + 0.5 * short[k][i] == requirement)

# Recruitment Limits
for k in range(K):
    for i in range(I):
        problem += recruit[k][i] <= data['recruit'][k]

# Overmanning Limit
problem += pulp.lpSum(overmanning[k][i] for k in range(K) for i in range(I)) <= data['num_overman']

# Short-time Working Limit
for k in range(K):
    for i in range(I):
        problem += short[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')