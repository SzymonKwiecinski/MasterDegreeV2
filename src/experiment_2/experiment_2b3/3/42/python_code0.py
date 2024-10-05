import pulp

# Data input
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

numdepot = data["numdepot"]
numport = data["numport"]
price = data["price"]
distance = data["distance"]

I = len(numdepot)
J = len(numport)

# Create problem
problem = pulp.LpProblem("Minimize_Transport_Cost", pulp.LpMinimize)

# Define variables
x = pulp.LpVariable.dicts("Containers", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([price * distance[i][j] * (x[i, j] / 2) for i in range(I) for j in range(J)])

# Constraints
for i in range(I):
    problem += pulp.lpSum([x[i, j] for j in range(J)]) <= numdepot[i]

for j in range(J):
    problem += pulp.lpSum([x[i, j] for i in range(I)]) == numport[j]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "number": [[pulp.value(x[i, j]) for j in range(J)] for i in range(I)]
}

# Display output
import json
print(json.dumps(output, indent=4))
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')