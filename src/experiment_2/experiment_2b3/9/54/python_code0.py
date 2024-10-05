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

# Unpack data
P = data["NumParts"]
M = data["NumMachines"]
time_required = data["TimeRequired"]
machine_costs = data["MachineCosts"]
availability = data["Availability"]
prices = data["Prices"]
min_batches = data["MinBatches"]
standard_cost = data["StandardCost"]
overtime_cost = data["OvertimeCost"]
overtime_hour = data["OvertimeHour"]

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]
machine1_hours = pulp.LpVariable('machine1_hours', lowBound=0, cat='Continuous')
overtime_hours1 = pulp.LpVariable('overtime_hours1', lowBound=0, cat='Continuous')

# Objective Function
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs_machines = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(1, M))
labor_costs = standard_cost * (machine1_hours - overtime_hours1) + overtime_cost * overtime_hours1

total_profit = revenue - costs_machines - labor_costs
problem += total_profit

# Constraints
# Hours on machine 1
problem += machine1_hours == pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
problem += machine1_hours <= overtime_hour[0] + overtime_hours1
problem += overtime_hours1 <= overtime_hour[0]

# Machine availability for other machines
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Solve
problem.solve()

# Output
batches_produced = [int(batches[p].varValue) for p in range(P)]
total_profit_value = pulp.value(total_profit)

output = {
    "batches": batches_produced,
    "total_profit": total_profit_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')