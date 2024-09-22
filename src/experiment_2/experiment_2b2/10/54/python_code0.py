from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value
import json

# Data from the problem description
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Extract data
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

# Create the LP problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Decision variables
batches = LpVariable.dicts("Batches", range(NumParts), lowBound=0, cat='Continuous')

# Objective function
profit = lpSum([Prices[p] * batches[p] for p in range(NumParts)])
labor_costs = (
    lpSum([TimeRequired[0][p] * batches[p] * StandardCost for p in range(NumParts)]) +
    OvertimeCost * lpSum([TimeRequired[0][p] * batches[p] for p in range(NumParts)] - OvertimeHour[0]) / OvertimeHour[0]
)

machine_costs = lpSum([
    MachineCosts[m] * lpSum([TimeRequired[m][p] * batches[p] for p in range(NumParts)]) 
    for m in range(1, NumMachines)
])

problem += profit - (labor_costs + machine_costs)

# Constraints
# Minimum batch constraint
for p in range(NumParts):
    problem += batches[p] >= MinBatches[p]

# Machine availability constraints
for m in range(1, NumMachines):
    problem += lpSum([TimeRequired[m][p] * batches[p] for p in range(NumParts)]) <= Availability[m]

# Solve the problem
problem.solve()

# Gather results
output = {
    "batches": [value(batches[p]) for p in range(NumParts)],
    "total_profit": value(problem.objective)
}

# Print the solution
print(json.dumps(output, indent=4))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')