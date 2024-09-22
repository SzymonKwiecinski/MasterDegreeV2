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

K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Initialize LP problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
z = pulp.LpVariable.dicts("z", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
r = pulp.LpVariable.dicts("r", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(
    data['costredundancy'][k] * r[k, i] +
    data['costoverman'][k] * z[k, i] +
    data['costshort'][k] * y[k, i]
    for k in range(K) for i in range(I)
)

# Constraints
for i in range(I):
    if i == 0:
        previous_balance = [data['strength'][k] for k in range(K)]
    else:
        previous_balance = [
            (1 - data['moreonewaste'][k]) * (
                (data['strength'][k] if i == 1 else data['requirement'][k][i-2]) + 
                pulp.value(previous_balance[k])
            )
            for k in range(K)
        ]

    # Manpower Balance
    for k in range(K):
        problem += ((1 - data['moreonewaste'][k]) * previous_balance[k] + 
                    x[k, i] * (1 - data['lessonewaste'][k]) + 
                    y[k, i] * 0.5 - 
                    r[k, i] >= data['requirement'][k][i] - z[k, i])

    # Recruitment Limits
    for k in range(K):
        problem += x[k, i] <= data['recruit'][k]

    # Overmanning Limits
    problem += pulp.lpSum(z[k, i] for k in range(K)) <= data['num_overman']

    # Short-time Working Limits
    for k in range(K):
        problem += y[k, i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')