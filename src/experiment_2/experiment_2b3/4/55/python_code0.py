import pulp

# The provided data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'standard_cost': 20, 
    'overtime_cost': 30, 
    'overtime_hour': 400, 
    'min_profit': 5000
}

# Variables from the data
time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
min_batches = data["min_batches"]
standard_cost = data["standard_cost"]
overtime_cost = data["overtime_cost"]
overtime_hour = data["overtime_hour"]
min_profit = data["min_profit"]

M = len(machine_costs)
P = len(prices)

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
machine_1_hours = pulp.LpVariable("machine_1_hours", lowBound=0)
overtime_hours = pulp.LpVariable("overtime_hours", lowBound=0)

# Objective: Maximize Profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - (
    pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(1, M)) +
    standard_cost * machine_1_hours + overtime_cost * overtime_hours
)
problem += profit

# Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_{m}_Capacity"

# Special constraints for Machine 1
problem += pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) == machine_1_hours + overtime_hours, "Machine_1_Usage"
problem += machine_1_hours <= overtime_hour, "Machine_1_Overtime_Limit"

# Minimum Profit
problem += profit >= min_profit, "Min_Profit"

# Solve the problem
problem.solve()

# Results
batches_produced = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')