import pulp

# Data extracted from <DATA>
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Number of different spare parts (K) and machines (S)
K = len(data['profit'])
S = len(data['capacity'])

# Initialize the Linear Program
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables: x_k -- Quantity of spare part k to produce
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Maximize total profit
problem += pulp.lpSum([data['profit'][k] * x[k] for k in range(K)]), "Total_Profit"

# Constraints: Time to produce each spare part must not exceed the available machine time
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s], f"Capacity_Constraint_Machine_{s}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')