import pulp
import json

# Load data
data_json = '''{
    "NumMachines": 3,
    "NumParts": 4,
    "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "MachineCosts": [160, 10, 15],
    "Availability": [200, 300, 500],
    "Prices": [570, 250, 585, 430],
    "MinBatches": [10, 10, 10, 10],
    "StandardCost": 20,
    "OvertimeCost": 30,
    "OvertimeHour": [400, 400, 300]
}'''
data = json.loads(data_json)

# Variables
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

# Create the LP problem
problem = pulp.LpProblem("AutoPartsMaxProfit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(num_parts), lowBound=0)

# Objective Function
total_time = pulp.lpSum([time_required[m][p] * batches[p] for m in range(num_machines) for p in range(num_parts)])

# Labor Cost Calculation
labor_cost = pulp.lpSum([
    standard_cost * total_time if total_time <= overtime_hour[m] else 
    (standard_cost * overtime_hour[m] + overtime_cost * (total_time - overtime_hour[m]))
    for m in range(num_machines)
])

# Define the objective function
problem += (pulp.lpSum([prices[p] * batches[p] for p in range(num_parts)]) 
            - pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) for m in range(num_machines)])
            - labor_cost), "Total Profit"

# Constraints
for m in range(num_machines):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) <= availability[m], f"MachineAvailability_{m}"

for p in range(num_parts):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')