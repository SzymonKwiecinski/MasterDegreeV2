import pulp

# Data from the JSON
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

# Indices
K = len(data['strength'])
I = len(data['requirement'][0])

# Problem definition
problem = pulp.LpProblem("Workforce_Management", pulp.LpMinimize)

# Decision Variables
r = pulp.LpVariable.dicts("recruits", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
o = pulp.LpVariable.dicts("overmanned", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
s = pulp.LpVariable.dicts("shortwork", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * max(0, data['strength'][k] - data['requirement'][k][i]) +
                      data['costoverman'][k] * o[(k, i)] +
                      data['costshort'][k] * s[(k, i)]
                      for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        problem += data['strength'][k] - data['lessonewaste'][k] * r[(k, i)] - data['moreonewaste'][k] * (data['strength'][k] - r[(k, i)]) + o[(k, i)] - s[(k, i)] == data['requirement'][k][i]

for k in range(K):
    for i in range(I):
        problem += r[(k, i)] <= data['recruit'][k]

for i in range(I):
    problem += pulp.lpSum(o[(k, i)] for k in range(K)) <= data['num_overman']

for k in range(K):
    for i in range(I):
        problem += s[(k, i)] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Display the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')