import pulp
import json

# Data from JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Number of parts and shops
K = len(data['profit'])
S = len(data['capacity'])

# Create the problem instance
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k+1}', lowBound=0) for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s], f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')