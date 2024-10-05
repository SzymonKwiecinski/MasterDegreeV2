import pulp

# Data
num_terminals = 3
num_destinations = 4
cost = [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]]
demand = [65, 70, 50, 45]
supply = [150, 100, 100]

# Indices for terminals, destinations, and ports
terminals = range(num_terminals)
destinations = range(num_destinations)
# In this example, let's assume ports are labeled the same as terminals for simplicity
ports = range(num_terminals)

# Create a list of all routes
routes = [(i, j) for i in range(num_terminals) for j in range(num_destinations)]

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(num_terminals), range(num_destinations)), lowBound=0, cat='Continuous')

# Initialize the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Objective function
problem += pulp.lpSum([cost[i][j] * x[i][j] for (i, j) in routes])

# Supply constraints for terminals
for k in terminals:
    problem += pulp.lpSum([x[k][j] for j in destinations]) <= supply[k]

# Demand constraints for destinations
for l in destinations:
    problem += pulp.lpSum([x[i][l] for i in terminals]) >= demand[l]

# Flow conservation for ports
# (In this example, flow conservation is not restrictive as we have no intermediate ports)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')