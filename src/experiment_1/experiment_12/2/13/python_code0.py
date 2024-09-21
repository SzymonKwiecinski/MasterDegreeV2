import pulp

# Data extracted from the provided json format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Parameters
K = len(data['profit'])   # Number of different spare parts
S = len(data['capacity']) # Number of machines

# Create a Linear Programming Problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K)), "Total Profit"

# Constraints
# 1. Quantities of each spare part must be non-negative (implicitly covered by lowBound=0 in variable definition)

# 2. Time to produce each spare part must not exceed the available machine time
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')