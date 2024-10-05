import pulp

# Data input
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

# Extracting data
M = data["NumMachines"]
P = data["NumParts"]
time_required = data["TimeRequired"]
machine_costs = data["MachineCosts"]
availability = data["Availability"]
prices = data["Prices"]
min_batches = data["MinBatches"]
standard_cost = data["StandardCost"]
overtime_cost = data["OvertimeCost"]
overtime_hour = data["OvertimeHour"]

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]
overtime_hours = pulp.LpVariable('overtime_hours', lowBound=0)

# Objective function
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
standard_machine_cost = pulp.lpSum((machine_costs[m] * time_required[m][p] * batches[p]) for m in range(1, M) for p in range(P))
outsourced_machine_cost = pulp.lpSum((time_required[0][p] * batches[p]) for p in range(P))
machine1_cost = (standard_cost * pulp.lpSum((time_required[0][p] * batches[p]) for p in range(P)) + 
                 (overtime_cost - standard_cost) * overtime_hours)

total_costs = standard_machine_cost + machine1_cost
problem += revenue - total_costs

# Constraints
# Machine time constraints for each machine (excluding machine 1)
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Overtime constraint for machine 1
problem += outsourced_machine_cost - overtime_hours <= overtime_hour[0]

# Solve the problem
problem.solve()

# Preparing output
batches_produced = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')