import pulp

# Parsing the data from the JSON format
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Number of depots and ports
I = len(numdepot)
J = len(numport)

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Transport_Cost", pulp.LpMinimize)

# Decision variables: number of containers to transport from depot i to port j
X = pulp.LpVariable.dicts("X", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function: Minimize the total cost
problem += pulp.lpSum(price * distance[i][j] * (X[(i, j)] / 2) for i in range(I) for j in range(J))

# Constraints: Supply constraints (containers available at depot)
for i in range(I):
    problem += pulp.lpSum(X[(i, j)] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Constraints: Demand constraints (containers needed at port)
for j in range(J):
    problem += pulp.lpSum(X[(i, j)] for i in range(I)) >= numport[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Collecting numbers of containers to be sent from each depot to each port
number = [[pulp.value(X[(i, j)]) for i in range(I)] for j in range(J)]

print({
    "number": number
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')