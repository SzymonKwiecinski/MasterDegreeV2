import pulp

# Data
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

# Parameters
K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Problem
problem = pulp.LpProblem("ManpowerPlanning", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Total workforce per category per year
total_workforce = pulp.LpVariable.dicts("total_workforce", ((k, i) for k in range(K) for i in range(I+1)), lowBound=0, cat='Continuous')

# Initial Strength Constraint
for k in range(K):
    problem += (total_workforce[k, 0] == data['strength'][k])

# Constraints
for k in range(K):
    for i in range(1, I + 1):
        wastage = (data['lessonewaste'][k] * recruit[k, i-1]) + (data['moreonewaste'][k] * total_workforce[k, i-1])
        problem += (total_workforce[k, i] == total_workforce[k, i-1] + recruit[k, i] - redundancy[k, i] - wastage)
        problem += (total_workforce[k, i] + overmanning[k, i] - short[k, i] / 2 >= data['requirement'][k][i-1])
        problem += (recruit[k, i] <= data['recruit'][k])
        problem += (short[k, i] <= data['num_shortwork'])

for i in range(I):
    problem += (pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman'])

# Objective Function
objective = pulp.lpSum([
    data['costredundancy'][k] * redundancy[k, i] +
    data['costoverman'][k] * overmanning[k, i] +
    data['costshort'][k] * short[k, i]
    for k in range(K) for i in range(I)
])

problem += objective

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')