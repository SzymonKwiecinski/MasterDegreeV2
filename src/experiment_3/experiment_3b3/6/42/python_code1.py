import pulp

# Data
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [
        [0.0, 2.0, 5.0],
        [2.0, 0.0, 3.0],
        [5.0, 3.0, 0.0]
    ]
}

num_depots = len(data['numdepot'])
num_ports = len(data['numport'])
price = data['price']
distances = data['distance']

# Problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous') for j in range(num_ports)] for i in range(num_depots)]

# Objective function
problem += pulp.lpSum((x[i][j] * distances[i][j] * price) / 2 for i in range(num_depots) for j in range(num_ports))

# Constraints

# Supply constraints
for i in range(num_depots):
    problem += pulp.lpSum(x[i][j] for j in range(num_ports)) <= data['numdepot'][i]

# Demand constraints
for j in range(num_ports):
    problem += pulp.lpSum(x[i][j] for i in range(num_depots)) >= data['numport'][j]

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')