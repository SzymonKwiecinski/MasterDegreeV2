import pulp

# Data from the JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

# Objective function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in range(data['NumProducts']))

# Constraints for each stage (machine)
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * quantity[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')