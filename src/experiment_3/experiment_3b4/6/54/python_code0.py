import pulp

# Extract data from the provided JSON format
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

# Decision Variables
x = [pulp.LpVariable(f'x_{p+1}', lowBound=data['MinBatches'][p], cat='Continuous') for p in range(data['NumParts'])]

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Cost for Machine 1
time_M1 = sum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))
cost_M1 = pulp.LpVariable('cost_M1', cat='Continuous')

# Define the cost_M1 as piecewise based on total time used on Machine 1
problem += cost_M1 == pulp.lpSum([data['StandardCost'] if time_M1 <= data['OvertimeHour'][0] 
                                  else data['OvertimeCost']] * time_M1)

# Objective Function
profit = (pulp.lpSum(data['Prices'][p] * x[p] for p in range(data['NumParts']))
          - pulp.lpSum(data['TimeRequired'][m][p] * x[p] * data['MachineCosts'][m]
                       for m in range(1, data['NumMachines'])
                       for p in range(data['NumParts']))
          - cost_M1)
problem += profit

# Constraints for machine availability for machines 2, 3, ..., M
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m]

# Solve the problem
problem.solve()

# Print the optimal value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')