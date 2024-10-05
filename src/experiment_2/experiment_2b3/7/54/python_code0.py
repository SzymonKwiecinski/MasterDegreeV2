import pulp

# Data
data = {
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
}

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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(NumParts), lowBound=0, cat='Continuous')
machine_hours = pulp.LpVariable.dicts("machine_hours", (range(1, NumMachines)), lowBound=0, cat='Continuous')

# Objective Function: Maximize Profit
revenue = pulp.lpSum([batches[p] * Prices[p] for p in range(NumParts)])
machine_costs = pulp.lpSum([machine_hours[m] * MachineCosts[m-1] for m in range(1, NumMachines)])
labor_cost = pulp.lpSum([pulp.lpSum([batches[p] * TimeRequired[0][p] for p in range(NumParts)]) * (StandardCost if pulp.lpSum([batches[p] * TimeRequired[0][p] for p in range(NumParts)]) <= OvertimeHour[0] else OvertimeCost)])

problem += revenue - machine_costs - labor_cost

# Constraints
# Minimum number of batches for each part
for p in range(NumParts):
    problem += batches[p] >= MinBatches[p]

# Machine constraints
for m in range(1, NumMachines):
    problem += machine_hours[m] == pulp.lpSum([batches[p] * TimeRequired[m][p] for p in range(NumParts)])
    problem += machine_hours[m] <= Availability[m]

# Solve the problem
problem.solve()

# Extracting the results
batches_produced = [pulp.value(batches[p]) for p in range(NumParts)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')