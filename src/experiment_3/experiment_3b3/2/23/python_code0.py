import pulp

# Define the data
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

K = len(data['strength'])  # Number of categories
I = len(data['requirement'][0])  # Number of years

# Initiate the problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum([data['costredundancy'][k] * max(0, data['strength'][k] - data['requirement'][k][i])
                       + data['costoverman'][k] * overmanning[k, i]
                       + data['costshort'][k] * short[k, i]
                       for k in range(K) for i in range(I)])

# Constraints
# Manpower balance
for k in range(K):
    for i in range(I):
        waste = (data['lessonewaste'][k] * recruit[k, i] + 
                 data['moreonewaste'][k] * (data['strength'][k] - recruit[k, i]))
        problem += (data['strength'][k] - waste
                    + recruit[k, i]
                    + overmanning[k, i]
                    - short[k, i] >= data['requirement'][k][i])

# Recruitment limit
for k in range(K):
    for i in range(I):
        problem += recruit[k, i] <= data['recruit'][k]

# Overmanning limit
problem += pulp.lpSum([overmanning[k, i] for k in range(K) for i in range(I)]) <= data['num_overman']

# Short-time working limit
for k in range(K):
    for i in range(I):
        problem += short[k, i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')