import pulp

# Data
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Index sets
I = len(numdepot)
J = len(numport)

# Problem
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Decision Variables
x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous') for j in range(J)] for i in range(I)]

# Objective Function
problem += pulp.lpSum((x[i][j] * distance[i][j] * price) for i in range(I) for j in range(J)) / 2

# Constraints

# Supply constraints at each depot
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i]

# Demand constraints at each port
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) >= numport[j]

# Solve the problem
problem.solve()

# Print the results
print("number:")
for i in range(I):
    print([pulp.value(x[i][j]) for j in range(J)])

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')