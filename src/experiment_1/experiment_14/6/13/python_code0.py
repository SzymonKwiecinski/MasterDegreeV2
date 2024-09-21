import pulp

# Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

K = len(data['profit'])  # Number of spare parts
S = len(data['capacity'])  # Number of machines

# Create a linear programming problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
# Constraint 1: Time to produce each spare part must not exceed the available machine time
for s in range(S):
    problem += (pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s]), f"Capacity_Constraint_Machine_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')