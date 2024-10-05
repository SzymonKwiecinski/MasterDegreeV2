import pulp

# Parse the input data
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Initialize the LP problem
problem = pulp.LpProblem("Minimize_Transport_Cost", pulp.LpMinimize)

# Variables: number of containers sent from depot i to port j
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective function: Minimize the total transportation cost
problem += pulp.lpSum((number[i, j] / 2) * price * distance[i][j] for i in range(I) for j in range(J))

# Constraints
# Supply constraints: Total containers sent from depot i should not exceed available containers in depot i
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= numdepot[i]

# Demand constraints: Total containers received at port j should be equal to the required containers in port j
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) == numport[j]

# Solve the problem
problem.solve()

# Extract the results
result = {"number": [[number[i, j].varValue for j in range(J)] for i in range(I)]}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')