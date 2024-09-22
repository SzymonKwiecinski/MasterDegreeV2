import pulp

# Data extraction from the provided JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Number of products and machines
K = data['NumProducts']  # Number of products
S = data['NumMachines']   # Number of stages/machines

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: quantity produced of each product
x = pulp.LpVariable.dicts("Produce", range(K), lowBound=0)

# Objective function: Maximize total profit
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(K)), "Total_Profit"

# Constraints for each stage
for s in range(S):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * x[k] for k in range(K)) <= data['AvailableTime'][s], f"Time_Constraint_Stage_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')