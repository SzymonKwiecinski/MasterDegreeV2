import pulp
import json

# Data in JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Indices
K = len(data['strength'])           # Number of manpower categories
I = len(data['requirement'][0])     # Number of years

# Create the linear programming problem
problem = pulp.LpProblem("ManpowerManagement", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - (data['lessonewaste'][k] * data['strength'][k] + data['moreonewaste'][k] * (data['strength'][k] - recruit[(k, i)]) ) ) + 
                data['costoverman'][k] * overmanning[(k, i)] +
                data['costshort'][k] * short[(k, i)] 
                for k in range(K) for i in range(I))

# Constraints
# Manpower balance
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - (data['lessonewaste'][k] * data['strength'][k] + 
                      data['moreonewaste'][k] * (data['strength'][k] - recruit[(k, i)])) + 
                      recruit[(k, i)] + overmanning[(k, i)] + 
                      0.5 * short[(k, i)] == data['requirement'][k][i])
        
# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += recruit[(k, i)] <= data['recruit'][k]

# Overmanning limit
problem += pulp.lpSum(overmanning[(k, i)] for k in range(K) for i in range(I)) <= data['num_overman']

# Short-time working limit
for k in range(K):
    for i in range(I):
        problem += short[(k, i)] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')