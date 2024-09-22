import pulp
import json

# Data provided in JSON format
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Extracting data
num_machines = data['NumMachines']
num_parts = data['NumParts']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0)

# Problem definition
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Objective Function
total_profit = pulp.lpSum([prices[p] * batches[p] for p in range(num_parts)]) \
               - pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) for m in range(num_machines)]) \
               - pulp.lpSum([
                    standard_cost * pulp.lpSum([availability[m] / pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) if pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) > 0 else 0 for m in range(num_machines)]) + 
                    overtime_cost * pulp.lpSum([pulp.lpMax(0, (availability[m] / pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) - overtime_hour[m])) for m in range(num_machines))
                ])

problem += total_profit

# Constraints
for m in range(num_machines):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) <= availability[m]

for p in range(num_parts):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')