import pulp

# Data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],  # Time to produce each product on each machine
    'AvailableTime': [200, 100],      # Available time on each machine
    'Profit': [20, 10]                # Profit from each product
}

# Define the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['NumProducts']), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumProducts'])), "Total_Profit"

# Constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][m] * x[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][m], f"Time_Constraint_Machine_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')