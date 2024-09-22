import pulp

# Data from JSON
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

K = len(data['strength'])  # Number of types
I = len(data['requirement'][0])  # Number of periods

# Initialize the problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
redundant = pulp.LpVariable.dicts("redundant", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Continuous')
employed = pulp.LpVariable.dicts("employed", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')

# Objective Function
objective = pulp.lpSum(data['costredundancy'][k] * redundant[(k, i)] +
                       data['costoverman'][k] * overmanning[(k, i)] +
                       data['costshort'][k] * short[(k, i)]
                       for k in range(K) for i in range(I))

problem += objective

# Constraints
# Initial manpower balance for the first period
for k in range(K):
    problem += (employed[(k, 0)] == data['strength'][k] * (1 - data['moreonewaste'][k]) + 
                recruit[(k, 0)] - redundant[(k, 0)])

# Manpower balance for subsequent periods
for k in range(K):
    for i in range(1, I):
        problem += (employed[(k, i)] == employed[(k, i-1)] * (1 - data['moreonewaste'][k]) + 
                    recruit[(k, i)] - redundant[(k, i)])

# Requirement satisfaction
for k in range(K):
    for i in range(I):
        problem += (employed[(k, i)] + overmanning[(k, i)] >= data['requirement'][k][i] - 0.5 * short[(k, i)])

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += (recruit[(k, i)] <= data['recruit'][k])

# Redundancy and Overmanning limits
for i in range(I):
    problem += (pulp.lpSum(overmanning[(k, i)] for k in range(K)) <= data['num_overman'])

# Short-time work limits
for k in range(K):
    for i in range(I):
        problem += (short[(k, i)] <= data['num_shortwork'])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')