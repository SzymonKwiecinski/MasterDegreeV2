import pulp

# Input data
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

# Extract data from input
numdepot = data["numdepot"]
numport = data["numport"]
price = data["price"]
distance = data["distance"]

# Number of depots and ports
I = len(numdepot)
J = len(numport)

# Create the problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables, number of containers from depot i to port j
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function: Minimize the total transportation cost
problem += pulp.lpSum(price * distance[i][j] * x[i, j] * 0.5 for i in range(I) for j in range(J))

# Constraints
# Total containers shipped from each depot cannot exceed availability
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i]

# Total containers received at each port must meet the requirement
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) == numport[j]

# Solve the problem
problem.solve()

# Prepare the output format
output = {
    "number": [[x[i, j].varValue for i in range(I)] for j in range(J)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')