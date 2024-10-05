import pulp

# Data from JSON
data = {
    'numdepot': [3, 3, 4], 
    'numport': [1, 6, 3], 
    'price': 3.0, 
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

I = len(data['numdepot'])
J = len(data['numport'])
price = data['price']
distances = data['distance']

# Create the problem
problem = pulp.LpProblem("TransportationCostMinimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(I) for j in range(J)], lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(0.5 * distances[i][j] * price * x[(i, j)] for i in range(I) for j in range(J))

# Supply constraints
for i in range(I):
    problem += pulp.lpSum(x[(i, j)] for j in range(J)) <= data['numdepot'][i]

# Demand constraints
for j in range(J):
    problem += pulp.lpSum(x[(i, j)] for i in range(I)) == data['numport'][j]

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')