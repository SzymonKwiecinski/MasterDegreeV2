import pulp
import json

# Data from the JSON format
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
num_parts = data['NumParts']
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(num_parts))
cost = pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(num_parts)) for m in range(data['NumMachines']))
problem += profit - cost, "Total_Profit"

# Machine Availability Constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(num_parts)) <= data['Availability'][m], f"Machine_Availability_{m}"

# Minimum Production Requirements
for p in range(num_parts):
    problem += batches[p] >= data['MinBatches'][p], f"Min_Batches_{p}"

# Labor Cost Constraint for Machine 1
overtime_hour = data['OvertimeHour'][0]
time_machine_1 = pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in range(num_parts))

# Standard and Overtime Cost calculation for Machine 1
cost_machine_1 = data['StandardCost'] * time_machine_1

problem += time_machine_1 <= overtime_hour, "Standard_Cost_Machine_1"
problem += time_machine_1 > overtime_hour, "Overtime_Cost_Machine_1"

# Solve the problem
problem.solve()

# Output results
batches_solution = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')