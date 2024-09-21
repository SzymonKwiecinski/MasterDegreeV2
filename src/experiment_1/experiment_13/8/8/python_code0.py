import pulp

# Data from the JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Number of products and machines
NumProducts = data['NumProducts']
NumMachines = data['NumMachines']

# Create the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(NumProducts), lowBound=0)

# Objective function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(NumProducts)), "Total_Profit"

# Constraints
for m in range(NumMachines):
    problem += pulp.lpSum(data['ProduceTime'][k][m] * x[k] for k in range(NumProducts)) <= data['AvailableTime'][m], f"Time_Constraint_Machine_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')