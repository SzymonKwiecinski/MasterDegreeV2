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

K = len(data['strength'])  # Number of categories
I = len(data['requirement'][0])  # Number of periods

# Problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
z = pulp.LpVariable.dicts("z", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    data['costredundancy'][k] * (data['strength'][k] + (x[k, i-1] if i > 0 else 0) - data['requirement'][k][i]) +
    data['costoverman'][k] * z[k, i] +
    data['costshort'][k] * y[k, i] +
    data['recruit'][k] * x[k, i]
    for k in range(K) for i in range(I)
)

# Constraints
for i in range(I):
    # Overmanning constraint
    problem += pulp.lpSum(z[k, i] for k in range(K)) <= data['num_overman'], f"Overman_Constraint_{i}"

    for k in range(K):
        # Manpower balance constraint
        problem += (data['strength'][k] +
                    (x[k, i-1] if i > 0 else 0) -
                    data['lessonewaste'][k] * x[k, i] -
                    data['moreonewaste'][k] * (data['strength'][k] - x[k, i]) ==
                    data['requirement'][k][i] + y[k, i] + z[k, i],
                    f"Manpower_Balance_{k}_{i}")

        # Short-time working limit
        problem += y[k, i] <= data['num_shortwork'], f"Shortwork_Limit_{k}_{i}"

        # Recruitment constraint
        problem += x[k, i] <= data['recruit'][k], f"Recruitment_Constraint_{k}_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')