import pulp

# Parse the input data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create variables for the quantity of each product to produce
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

# Set objective function to maximize total profit
problem += pulp.lpSum(data['Profit'][k] * quantities[k] for k in range(data['NumProducts']))

# Add constraints for each machine's available time
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * quantities[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][s]

# Solve the problem
problem.solve()

# Extract the solution
solution = {
    "quantity": [pulp.value(quantities[k]) for k in range(data['NumProducts'])]
}

print(solution)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')