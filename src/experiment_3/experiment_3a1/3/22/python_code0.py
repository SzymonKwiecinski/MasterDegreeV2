import pulp

# Data from the provided JSON
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

K = len(data['strength'])  # number of manpower categories
I = len(data['requirement'][0])  # number of years

# Create the problem
problem = pulp.LpProblem("Manpower Management", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - 
    data['lessonewaste'][k] * recruit_vars[k][i] - 
    data['moreonewaste'][k] * data['strength'][k] + 
    overmanning_vars[k][i] - short_vars[k][i]) for k in range(K) for i in range(I))

# Constraints
# Manpower Requirement Satisfaction
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - 
                     data['lessonewaste'][k] * recruit_vars[k][i] - 
                     data['moreonewaste'][k] * data['strength'][k] + 
                     overmanning_vars[k][i] - short_vars[k][i] >= 
                     data['requirement'][k][i])

# Recruitment Limit
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k][i] <= data['recruit'][k]

# Overmanning Limit
for i in range(I):
    problem += pulp.lpSum(overmanning_vars[k][i] for k in range(K)) <= data['num_overman']

# Short-time Working Limit
for k in range(K):
    for i in range(I):
        problem += short_vars[k][i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')