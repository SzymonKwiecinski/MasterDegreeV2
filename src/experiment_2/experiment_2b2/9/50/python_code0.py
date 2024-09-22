from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus
import json

# Input data
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10], 
    "extra_costs": [0, 15, 22.5], 
    "max_extra": [0, 80, 80]
}

# Parse data
time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
min_batches = data["min_batches"]
extra_costs = data["extra_costs"]
max_extra = data["max_extra"]

P = len(prices)  # Number of parts
M = len(availability)  # Number of machines

# Create LP problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Decision variables
batches = [LpVariable(f'batches_{p+1}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]
extra_time = [LpVariable(f'extra_time_{m+1}', lowBound=0, upBound=max_extra[m], cat='Continuous') for m in range(M)]

# Objective function
profit = lpSum([
    prices[p] * batches[p] for p in range(P)
]) - lpSum([
    (machine_costs[m] * (availability[m] + extra_time[m]) + extra_costs[m] * extra_time[m]) for m in range(M)
])
problem += profit, "Total Profit"

# Constraints
for m in range(M):
    problem += lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] + extra_time[m], f"Machine_{m+1}_Capacity"

# Solve problem
problem.solve()

# Fetch results
batches_produced = [batches[p].varValue for p in range(P)]
extra_time_purchased = [extra_time[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

result = {
    "batches": batches_produced,
    "extra_time": extra_time_purchased,
    "total_profit": total_profit
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')