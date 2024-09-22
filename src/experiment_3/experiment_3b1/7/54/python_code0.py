import pulp
import json

# Load the data
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Extract data from the loaded json
NumMachines = data['NumMachines']
NumParts = data['NumParts']
TimeRequired = data['TimeRequired']
MachineCosts = data['MachineCosts']
Availability = data['Availability']
Prices = data['Prices']
MinBatches = data['MinBatches']
StandardCost = data['StandardCost']
OvertimeCost = data['OvertimeCost']
OvertimeHour = data['OvertimeHour']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
batches = [pulp.LpVariable(f'batch_{p}', lowBound=0) for p in range(NumParts)]

# Define the objective function
profit_expr = pulp.lpSum([Prices[p] * batches[p] for p in range(NumParts)]) \
               - pulp.lpSum([MachineCosts[m] * (pulp.lpSum([TimeRequired[m][p] * batches[p] for p in range(NumParts)])) for m in range(NumMachines)])

problem += profit_expr, "Total_Profit"

# Constraints for each machine
for m in range(1, NumMachines):
    problem += (pulp.lpSum([TimeRequired[m][p] * batches[p] for p in range(NumParts)]) <= Availability[m]), f"Machine_{m}_Availability"

# Constraint for machine 1
problem += (pulp.lpSum([TimeRequired[0][p] * batches[p] for p in range(NumParts)]) <= OvertimeHour[0]), "Machine_1_Overtime"

# Handle overtime cost for machine 1
overtime_expr = pulp.lpSum([TimeRequired[0][p] * batches[p] for p in range(NumParts)]) - OvertimeHour[0]
problem += (overtime_expr >= 0), "Overtime_Condition"

# Minimum batches constraints
for p in range(NumParts):
    problem += (batches[p] >= MinBatches[p]), f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Extract results
batches_result = [pulp.value(batch) for batch in batches]
total_profit = pulp.value(problem.objective)

# Output results
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')