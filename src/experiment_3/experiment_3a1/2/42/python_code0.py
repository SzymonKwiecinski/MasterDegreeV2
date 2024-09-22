import pulp

# Data from the provided JSON format
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

num_depots = len(data['numdepot'])
num_ports = len(data['numport'])

# Create a linear programming problem
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(num_depots), range(num_ports)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((x[i][j] / 2) * data['distance'][i][j] * data['price'] for i in range(num_depots) for j in range(num_ports)), "Total_Transportation_Cost"

# Supply Constraints
for i in range(num_depots):
    problem += pulp.lpSum(x[i][j] for j in range(num_ports)) <= data['numdepot'][i], f"Supply_Constraint_{i}"

# Demand Constraints
for j in range(num_ports):
    problem += pulp.lpSum(x[i][j] for i in range(num_depots)) >= data['numport'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')