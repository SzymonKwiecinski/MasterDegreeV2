import pulp

# Extract data from the json format
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

# Create the Linear Programming Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create a list of decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(data['NumParts'])]

# Calculate T_1 for labor costs
T_1 = pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))

# Calculate Labor Costs condition
labor_costs = pulp.LpVariable('labor_costs', lowBound=0, cat='Continuous')
problem += labor_costs == pulp.lpSum([
    data['StandardCost'] * T_1 if T_1 <= data['OvertimeHour'][0] else 
    (data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * (T_1 - data['OvertimeHour'][0]))
])

# Create the objective function
profit = (
    pulp.lpSum(data['Prices'][p] * x[p] for p in range(data['NumParts'])) -
    pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) for m in range(data['NumMachines'])) -
    labor_costs
)
problem += profit

# Add constraints for minimum batch requirements
for p in range(data['NumParts']):
    problem += x[p] >= data['MinBatches'][p]

# Add constraints for machine availability
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')