import pulp

# Data input
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Unpack data
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  # Number of depots
J = len(numport)   # Number of ports

# Initialize the problem
problem = pulp.LpProblem("Transport_Empty_Containers", pulp.LpMinimize)

# Decision variables: number of containers sent from depot i to port j
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function: Minimize total transportation cost
problem += pulp.lpSum(price * distance[i][j] * (x[(i, j)] // 2) for i in range(I) for j in range(J))

# Constraints
# Supply constraints: Number of containers from depot i
for i in range(I):
    problem += pulp.lpSum(x[(i, j)] for j in range(J)) <= numdepot[i]

# Demand constraints: Number of containers needed at port j
for j in range(J):
    problem += pulp.lpSum(x[(i, j)] for i in range(I)) == numport[j]

# Solve the problem
problem.solve()

# Retrieve results
result = {
    "number": [[pulp.value(x[(i, j)]) for i in range(I)] for j in range(J)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')