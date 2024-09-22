import pulp

# Read data from JSON format
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Get the number of depots and ports
I = len(numdepot)
J = len(numport)

# Define the LP problem
problem = pulp.LpProblem("Minimize_Transport_Cost", pulp.LpMinimize)

# Define the decision variables
# x[i][j] is the number of containers sent from depot i to port j
x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0, cat='Integer') for j in range(J)] for i in range(I)]

# Objective function: Minimize total transportation cost
problem += pulp.lpSum(x[i][j] * price * distance[i][j] / 2 for i in range(I) for j in range(J))

# Constraints: The number of containers sent from each depot cannot exceed the available containers
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i]

# Constraints: The number of containers received at each port must satisfy the demand
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) == numport[j]

# Solve the LP problem
problem.solve()

# Format the result for output
result = {
    "number": [[pulp.value(x[i][j]) for j in range(J)] for i in range(I)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')