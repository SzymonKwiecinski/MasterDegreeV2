import pulp

# Data
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

num_depot = data['numdepot']
num_port = data['numport']
price = data['price']
distance = data['distance']

I = len(num_depot)
J = len(num_port)

# Define the problem
problem = pulp.LpProblem("Transportation", pulp.LpMinimize)

# Define decision variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), 
                               lowBound=0, cat='Integer')

# Objective function
total_cost = pulp.lpSum([
    number[i, j] / 2 * price * distance[i][j] for i in range(I) for j in range(J)
])
problem += total_cost

# Constraints
# Supply constraints
for i in range(I):
    problem += pulp.lpSum([number[i, j] for j in range(J)]) <= num_depot[i]

# Demand constraints
for j in range(J):
    problem += pulp.lpSum([number[i, j] for i in range(I)]) >= num_port[j]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "number": [[pulp.value(number[i, j]) for j in range(J)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')