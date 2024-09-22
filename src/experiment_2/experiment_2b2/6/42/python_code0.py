import pulp

# Parse the input data
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data["numdepot"]
numport = data["numport"]
price = data["price"]
distance = data["distance"]

I = len(numdepot)
J = len(numport)

# Initialize the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Create decision variables
x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0, cat='Integer') for j in range(J)] for i in range(I)]

# Objective function: Minimize total transportation cost
cost = pulp.lpSum(x[i][j] * price * distance[i][j] for i in range(I) for j in range(J))
problem += cost

# Constraints

# Each depot cannot send more containers than it has
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i]

# Each port must receive exactly the number of containers it requires
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) == numport[j]

# Each barge can contain exactly two containers
for i in range(I):
    for j in range(J):
        problem += x[i][j] % 2 == 0

# Solve the problem
problem.solve()

# Extract the results
number = [[pulp.value(x[i][j]) for j in range(J)] for i in range(I)]

result = {
    "number": number
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')