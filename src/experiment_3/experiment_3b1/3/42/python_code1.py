import pulp

# Data from the provided JSON
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Sets
I = range(len(data['numdepot']))  # Depots
J = range(len(data['numport']))    # Ports

# Create the problem
problem = pulp.LpProblem("ContainerTransport", pulp.LpMinimize)

# Decision Variables
number = pulp.LpVariable.dicts("number", (I, J), lowBound=0)

# Objective Function
problem += pulp.lpSum((number[i][j] * data['price'] * data['distance'][i][j]) / 2 for i in I for j in J)

# Supply Constraints
for i in I:
    problem += pulp.lpSum(number[i][j] for j in J) <= data['numdepot'][i], f"Supply_Constraint_{i}"

# Demand Constraints
for j in J:
    problem += pulp.lpSum(number[i][j] for i in I) == data['numport'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')