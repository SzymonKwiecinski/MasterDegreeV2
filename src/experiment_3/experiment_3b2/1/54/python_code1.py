import pulp
import json

# Data input
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(1, data['NumParts'] + 1), lowBound=0, cat='Continuous')

# Objective Function
total_profit = pulp.lpSum(data['Prices'][p - 1] * batches[p] for p in range(1, data['NumParts'] + 1))

# Machine Costs and Overtime Calculations
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour'][0]  # Assuming working with the first machine for overtime calculations

# Machine cost calculation
machine_costs = pulp.lpSum(data['MachineCosts'][m - 1] * pulp.lpSum(data['TimeRequired'][m - 1][p - 1] * batches[p] for p in range(1, data['NumParts'] + 1)) for m in range(2, data['NumMachines'] + 1))

# Overtime cost calculation
total_time = pulp.lpSum(data['TimeRequired'][0][p - 1] * batches[p] for p in range(1, data['NumParts'] + 1))
overtime_cost_calculation = (overtime_cost * pulp.lpSum([max(0, total_time - overtime_hour)]))

# Standard machine cost calculation
standard_cost_calculation = standard_cost * pulp.lpMin(total_time, overtime_hour)

# Complete objective function
problem += (total_profit - machine_costs - standard_cost_calculation - overtime_cost_calculation)

# Constraints
# 1. Machine availability constraints
for m in range(2, data['NumMachines'] + 1):
    problem += (pulp.lpSum(data['TimeRequired'][m - 1][p - 1] * batches[p] for p in range(1, data['NumParts'] + 1)) <= data['Availability'][m - 1])

# 2. Minimum batches required
for p in range(1, data['NumParts'] + 1):
    problem += (batches[p] >= data['MinBatches'][p - 1])

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')