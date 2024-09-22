import pulp

# Data
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [
        [0.0, 2.0, 5.0],
        [2.0, 0.0, 3.0],
        [5.0, 3.0, 0.0]
    ]
}

# Indices
I = len(data['numdepot'])
J = len(data['numport'])

# Problem
problem = pulp.LpProblem("ContainerTransportation", pulp.LpMinimize)

# Decision Variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    (number[i, j] / 2) * data['distance'][i][j] * data['price']
    for i in range(I) for j in range(J)
)

# Constraints
# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= data['numdepot'][i]

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= data['numport'][j]

# Solve Problem
problem.solve()

# Output
output = {'number': [[pulp.value(number[i, j]) for i in range(I)] for j in range(J)]}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')