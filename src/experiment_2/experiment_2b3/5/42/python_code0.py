import pulp

# Data from the provided json input
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Number of depots and ports
I = len(numdepot)
J = len(numport)

# Initialize the LP problem
problem = pulp.LpProblem("Transportation_Cost_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(x[i, j] * price * distance[i][j] / 2 for i in range(I) for j in range(J))

# Subject to supply constraints
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Subject to demand constraints
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= numport[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Construct the output
output = {"number": [[pulp.value(x[i, j]) for i in range(I)] for j in range(J)]}

# Printing the result
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')