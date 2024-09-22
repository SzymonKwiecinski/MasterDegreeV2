import pulp

# Data
data = {
    'numdepot': [3, 3, 4], 
    'numport': [1, 6, 3], 
    'price': 3.0, 
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Parameters
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Sets
I = range(len(numdepot))  # Depots
J = range(len(numport))    # Ports

# Create the LP problem
problem = pulp.LpProblem("ContainerTransportation", pulp.LpMinimize)

# Decision Variables
number = pulp.LpVariable.dicts("number", (I, J), lowBound=0)

# Objective Function
problem += pulp.lpSum((number[i][j] / 2) * distance[i][j] * price for i in I for j in J)

# Constraints
# Supply constraints
for i in I:
    problem += pulp.lpSum(number[i][j] for j in J) <= numdepot[i]

# Demand constraints
for j in J:
    problem += pulp.lpSum(number[i][j] for i in I) >= numport[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')