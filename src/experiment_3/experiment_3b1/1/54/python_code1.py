import pulp
import json

# Data provided in JSON format
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

# Create the problem instance
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision variables: batches produced for each part
batches = pulp.LpVariable.dicts("Batches", range(NumParts), lowBound=0)

# Objective function: Maximize total profit
total_hours = pulp.lpSum(TimeRequired[m][p] * batches[p] for m in range(NumMachines) for p in range(NumParts))
labor_cost = pulp.lpSum(
    [StandardCost * min(total_hours, OvertimeHour[m]) +
     OvertimeCost * max(0, total_hours - OvertimeHour[m]) for m in range(NumMachines)]
)

profit = pulp.lpSum(Prices[p] * batches[p] for p in range(NumParts)) - \
         pulp.lpSum(MachineCosts[m] * pulp.lpSum(TimeRequired[m][p] * batches[p] for p in range(NumParts)) for m in range(NumMachines)) - labor_cost

problem += profit

# Constraints: Production constraints per machine
for m in range(NumMachines):
    problem += pulp.lpSum(TimeRequired[m][p] * batches[p] for p in range(NumParts)) <= Availability[m]

# Minimum production requirements
for p in range(NumParts):
    problem += batches[p] >= MinBatches[p]

# Solve the problem
problem.solve()

# Output the solution
for p in range(NumParts):
    print(f'Batches of part {p+1}: {batches[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')