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

K = len(data['strength'])
I = len(data['requirement'][0])

# Problem
problem = pulp.LpProblem("Manpower_Requirements", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
redundant = pulp.LpVariable.dicts("Redundant", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * redundant[k, i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] +
                    sum(recruit[k, j] - redundant[k, j] - data['moreonewaste'][k] * data['strength'][k] - data['lessonewaste'][k] * recruit[k, j] for j in range(i + 1)) +
                    overmanning[k, i] +
                    0.5 * short[k, i] == data['requirement'][k][i])

        problem += recruit[k, i] <= data['recruit'][k]
        problem += short[k, i] <= data['num_shortwork']

problem += pulp.lpSum(overmanning[k, i] for k in range(K) for i in range(I)) <= data['num_overman']

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')