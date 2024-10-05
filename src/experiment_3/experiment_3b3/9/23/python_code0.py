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
K = len(data['strength'])
I = len(data['requirement'][0])

# Problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
manpower = pulp.LpVariable.dicts("manpower", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(
    data['costredundancy'][k] * recruit[k, i] +
    data['costoverman'][k] * overmanning[k, i] +
    data['costshort'][k] * short[k, i]
    for k in range(K) for i in range(I)
)

# Constraints

# Manpower Balance
for k in range(K):
    for i in range(I):
        problem += (manpower[k, i] ==
                    data['strength'][k] - 
                    data['lessonewaste'][k] * data['strength'][k] - 
                    data['moreonewaste'][k] * (data['strength'][k] - recruit[k, i]) + 
                    recruit[k, i] + 
                    overmanning[k, i] - 
                    short[k, i] / 2)

# Recruitment Limit
for k in range(K):
    for i in range(I):
        problem += recruit[k, i] <= data['recruit'][k]

# Overmanning Limit
problem += pulp.lpSum(overmanning[k, i] for k in range(K) for i in range(I)) <= data['num_overman']

# Short-time Working Limit
for k in range(K):
    for i in range(I):
        problem += short[k, i] <= data['num_shortwork']

# Manpower Requirement
for k in range(K):
    for i in range(I):
        problem += manpower[k, i] >= data['requirement'][k][i] - overmanning[k, i]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')