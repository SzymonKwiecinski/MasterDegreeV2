import pulp

# Data from JSON
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

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=data['MinBatches'][p], cat='Continuous') for p in range(data['NumParts'])]

# Objective function
revenue = pulp.lpSum(data['Prices'][p] * x[p] for p in range(data['NumParts']))
costs = pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) for m in range(1, data['NumMachines']))

# Machine 1 cost handling
h1 = pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))
cost_1 = (
    (data['StandardCost'] * h1) 
    + (data['OvertimeCost'] * (h1 - data['OvertimeHour'][0]))
    * (h1 > data['OvertimeHour'][0])
)

# Full objective function
problem += revenue - costs - cost_1

# Constraints
# Machine 2 and onward availability constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')