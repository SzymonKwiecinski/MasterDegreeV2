import pulp

# Data input
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Define the problem
problem = pulp.LpProblem("Minimize_Transport_Cost", pulp.LpMinimize)

# Decision Variables
# x[i][j] means the number of containers sent from depot i to port j
x = pulp.LpVariable.dicts("x",
                          ((i, j) for i in range(I) for j in range(J)),
                          lowBound=0,
                          cat='Integer')

# Objective Function: Minimize the total transportation cost
problem += pulp.lpSum((price * distance[i][j] * (x[i, j] / 2)) for i in range(I) for j in range(J))

# Constraints
# Each depot must not send more containers than it has
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i]

# Each port must receive the required number of containers
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) == numport[j]

# Solve the problem
problem.solve()

# Prepare the output
solution = {"number": [[pulp.value(x[i, j]) for j in range(J)] for i in range(I)]}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')