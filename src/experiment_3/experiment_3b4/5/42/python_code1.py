import pulp

# Data from the problem
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

# Create a Linear Programming Minimization Problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(num_depots) for j in range(num_ports)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((x[i, j] * data['price'] * data['distance'][i][j] / 2) for i in range(num_depots) for j in range(num_ports))

# Constraints
# Supply constraints
for i in range(num_depots):
    problem += pulp.lpSum(x[i, j] for j in range(num_ports)) <= data['numdepot'][i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(num_ports):
    problem += pulp.lpSum(x[i, j] for i in range(num_depots)) == data['numport'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')