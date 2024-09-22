import pulp

# Define the data
data = {
    'NumMachines': 3,
    'NumParts': 4,
    'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'MachineCosts': [160, 10, 15],
    'Availability': [200, 300, 500],
    'Prices': [570, 250, 585, 430],
    'MinBatches': [10, 10, 10, 10],
    'StandardCost': 20,
    'OvertimeCost': 30,
    'OvertimeHour': [400, 400, 300]
}

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f"x_{p}", lowBound=data['MinBatches'][p], cat='Continuous') for p in range(data['NumParts'])]

# Calculate the LaborCost
labor_hours = sum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))
if_condition = labor_hours <= data['OvertimeHour'][0]
labor_cost = (
    data['StandardCost'] * labor_hours +
    (data['OvertimeCost'] - data['StandardCost']) * pulp.lpSum([x[p] for p in range(data['NumParts'])]) * (1 - if_condition)
)

# Define the objective function
profit = pulp.lpSum(data['Prices'][p] * x[p] for p in range(data['NumParts']))
operational_costs = pulp.lpSum(
    data['TimeRequired'][m][p] * x[p] * data['MachineCosts'][m] for m in range(1, data['NumMachines']) for p in range(data['NumParts'])
)
objective = profit - (operational_costs + labor_cost)

# Set the objective
problem += objective

# Add constraints for each machine
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m]

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')