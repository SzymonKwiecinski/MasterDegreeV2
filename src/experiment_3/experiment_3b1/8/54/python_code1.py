import pulp
import json

# Load data from JSON format
data = {'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 
        'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 
        'OvertimeHour': [400, 400, 300]}

# Define the problem
problem = pulp.LpProblem("AutoPartsMaxProfit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(data['NumParts']), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts']))
cost = pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(data['NumMachines']))
problem += profit - cost, "TotalProfit"

# Constraints for machine time availability
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"TimeAvailableMachine{m}"

# Minimum production constraints
for p in range(data['NumParts']):
    problem += batches[p] >= data['MinBatches'][p], f"MinBatchesPart{p}"

# Labor cost constraints for Machine 1
machine_index = 0  # Assuming the first machine is the one with labor constraints
for p in range(data['NumParts']):
    production_time = data['TimeRequired'][machine_index][p] * batches[p]
    problem += production_time <= data['OvertimeHour'][machine_index], f"CostWhenWithinOvertime_Part{p}"
    problem += production_time >= data['OvertimeHour'][machine_index], f"CostWhenExceedsOvertime_Part{p}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')