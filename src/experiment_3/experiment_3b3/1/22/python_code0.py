import pulp

# Create a linear programming problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

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

K = len(data['strength'])
I = len(data['requirement'][0])

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * redundancy[k, i] for k in range(K) for i in range(I))

# Constraints

# Manpower Balance
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k]
                    - data['lessonewaste'][k] * recruit[k, i]
                    - data['moreonewaste'][k] * (data['strength'][k] - redundancy[k, i])
                    + overmanning[k, i]
                    + 0.5 * short[k, i]
                    >= data['requirement'][k][i])

# Recruitment Limit
for k in range(K):
    problem += pulp.lpSum(recruit[k, i] for i in range(I)) <= data['recruit'][k]

# Overmanning Limit
for k in range(K):
    problem += pulp.lpSum(overmanning[k, i] for i in range(I)) <= data['num_overman']

# Short-time Working Limit
for k in range(K):
    problem += pulp.lpSum(short[k, i] for i in range(I)) <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')