import pulp

# Data provided
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Extracting values from the data
time = data['time']
profit = data['profit']
capacity = data['capacity']
K = len(profit)  # Number of products
S = len(capacity)  # Number of capacities

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Objective"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Display the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')