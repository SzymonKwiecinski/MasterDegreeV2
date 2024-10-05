import pulp

# Data
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Indices
I = len(numdepot)
J = len(numport)

# Problem
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat=pulp.LpInteger)

# Objective Function
problem += pulp.lpSum((price * distance[i][j] / 2) * x[i, j] for i in range(I) for j in range(J))

# Constraints
# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i]

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= numport[j]

# Barge Constraints
for i in range(I):
    for j in range(J):
        problem += x[i, j] % 2 == 0  # This line needs to enforce x[i, j] is even differently

# Enforce even constraint using an auxiliary variable
even = pulp.LpVariable.dicts("even", ((i, j) for i in range(I) for j in range(J)), cat=pulp.LpBinary)
for i in range(I):
    for j in range(J):
        problem += x[i, j] == 2 * even[i, j]

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')