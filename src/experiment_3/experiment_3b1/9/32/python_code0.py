import pulp

# Data from the provided JSON
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Number of products and machines
K = data['NumProducts']
S = data['NumMachines']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
profit_expr = pulp.lpSum(data['Profit'][k] * x[k] for k in range(K))
problem += profit_expr, "Total_Profit"

# Constraints for each stage
for s in range(S):
    problem += (pulp.lpSum(data['ProduceTime'][k][s] * x[k] for k in range(K)) <= data['AvailableTime'][s]), f"Time_Constraint_{s + 1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')