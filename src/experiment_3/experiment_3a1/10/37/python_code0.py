import pulp

# Data extracted from the provided JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Define problem
K = len(data['profit'])  # Number of spare parts
S = len(data['capacity'])  # Number of shops

# Create the linear programming problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K)), "Total Profit"

# Constraints
for s in range(S):
    problem += (pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s]), f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')