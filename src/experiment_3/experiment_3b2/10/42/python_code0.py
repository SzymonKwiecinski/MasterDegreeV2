import pulp
import json

# Data in JSON format
data = json.loads('{"numdepot": [3, 3, 4], "numport": [1, 6, 3], "price": 3.0, "distance": [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}')

# Extract data
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum((x[i, j] / 2) * distance[i][j] * price for i in range(I) for j in range(J))

# Constraints
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i]

for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= numport[j]

# x_ij must be an even integer
for i in range(I):
    for j in range(J):
        problem += x[i, j] % 2 == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')