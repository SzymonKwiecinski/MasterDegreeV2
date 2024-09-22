import pulp

# Problem Data
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
K = len(data['strength'])  # Number of categories
I = len(data['requirement'][0])  # Number of years

# Problem
problem = pulp.LpProblem("ManpowerPlanning", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
z = pulp.LpVariable.dicts("z", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
y = pulp.LpVariable.dicts("y", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=data['num_shortwork'], cat='Integer')
w = pulp.LpVariable.dicts("w", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=data['num_overman'], cat='Integer')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * z[k, i] + data['costoverman'][k] * w[k, i] + data['costshort'][k] * y[k, i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            problem += (data['strength'][k] - z[k, i] + x[k, i] - data['moreonewaste'][k] * (data['strength'][k] - z[k, i]) ==
                        data['requirement'][k][i] - 0.5 * y[k, i] - w[k, i])
        else:
            problem += (x[k, i] + data['strength'][k] - z[k, i] - data['moreonewaste'][k] * (data['strength'][k] - z[k, i]) +
                        data['lessonewaste'][k] * x[k, i - 1] ==
                        data['requirement'][k][i] - 0.5 * y[k, i] - w[k, i])
        problem += x[k, i] <= data['recruit'][k]

# Solve
problem.solve()

# Output Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')