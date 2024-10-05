import pulp

# Data
data = {
    "numdepot": [3, 3, 4],
    "numport": [1, 6, 3],
    "price": 3.0,
    "distance": [
        [0.0, 2.0, 5.0],
        [2.0, 0.0, 3.0],
        [5.0, 3.0, 0.0]
    ]
}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Create the problem
problem = pulp.LpProblem("MinimizeTransportationCosts", pulp.LpMinimize)

# Decision variables
number = [
    [pulp.LpVariable(f'number_{i}_{j}', lowBound=0, cat='Integer') for j in range(J)]
    for i in range(I)
]

# Objective function
problem += pulp.lpSum(
    (distance[i][j] * price) * (number[i][j] / 2) for i in range(I) for j in range(J)
)

# Constraints
# Supply constraints
for i in range(I):
    problem += pulp.lpSum(number[i][j] for j in range(J)) <= numdepot[i]

# Demand constraints
for j in range(J):
    problem += pulp.lpSum(number[i][j] for i in range(I)) >= numport[j]

# Solve the problem
problem.solve()

# Retrieve results
result = {
    "number": [[pulp.value(number[i][j]) for j in range(J)] for i in range(I)]
}

print(result)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')