import pulp

# Define data
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

# Define the problem
problem = pulp.LpProblem("Minimize Redundancy Costs", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("Recruits", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
z = pulp.LpVariable.dicts("ShortWorking", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function
objective = pulp.lpSum([
    data['costredundancy'][k] * (
        data['strength'][k] + pulp.lpSum([
            x[k, j] - (
                data['lessonewaste'][k] * x[k, j] +
                data['moreonewaste'][k] * (data['strength'][k] - x[k, j])
            )
            for j in range(i)
        ]) - data['requirement'][k][i]
    )
    for k in range(K) for i in range(I)
])

problem += objective

# Constraints
for k in range(K):
    for i in range(I):
        problem += (
            data['strength'][k] + pulp.lpSum([
                x[k, j] - (
                    data['lessonewaste'][k] * x[k, j] +
                    data['moreonewaste'][k] * (data['strength'][k] - x[k, j])
                )
                for j in range(i)
            ]) + y[k, i] + 0.5 * z[k, i] >= data['requirement'][k][i]
        )

        problem += x[k, i] <= data['recruit'][k]
        problem += z[k, i] <= data['num_shortwork']

for i in range(I):
    problem += pulp.lpSum([y[k, i] for k in range(K)]) <= data['num_overman']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')