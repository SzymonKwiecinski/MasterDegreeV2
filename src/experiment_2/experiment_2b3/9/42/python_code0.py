import pulp

# Load data
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Unpack data
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Initialize the problem
problem = pulp.LpProblem("Minimize_Transport_Cost", pulp.LpMinimize)

# Define decision variables
x = [[pulp.LpVariable(f'x_{i}_{j}', lowBound=0, cat='Integer') for j in range(J)] for i in range(I)]

# Objective function: Minimize total cost
problem += pulp.lpSum(price * (distance[i][j]) * (x[i][j] / 2) for i in range(I) for j in range(J))

# Constraints
# Container supply constraints for depots
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i]

# Container demand constraints for ports
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) >= numport[j]

# Solve the problem
problem.solve()

# Prepare the result
result = {"number": [[pulp.value(x[i][j]) for j in range(J)] for i in range(I)]}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')