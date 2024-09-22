import pulp

# Data from JSON
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

# Problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((x[i, j] * price * distance[i][j]) / 2 for i in range(I) for j in range(J))

# Constraints
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= num_depot[i]

for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= num_port[j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')