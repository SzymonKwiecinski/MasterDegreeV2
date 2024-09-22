import pulp

# Data from JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(data['NumProducts']), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in range(data['NumProducts'])), "Total_Profit"

# Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * quantity[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][s], f"Time_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')