import pulp

# Retrieve data
data = {
    'NumMachines': 3, 
    'NumParts': 4, 
    'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'MachineCosts': [160, 10, 15], 
    'Availability': [200, 300, 500], 
    'Prices': [570, 250, 585, 430], 
    'MinBatches': [10, 10, 10, 10], 
    'StandardCost': 20, 
    'OvertimeCost': 30, 
    'OvertimeHour': [400, 400, 300]
}

# Extracting data
M = data['NumMachines']
P = data['NumParts']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Define the problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", (range(P)), lowBound=0, cat='Continuous')

# Constraints
for m in range(1, M):
    problem += (
        pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], 
        f"Machine_{m}_availability"
    )

# Overtime constraints for machine 0
machine_1_usage = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
problem += machine_1_usage <= overtime_hour[0]

# Objective function
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
machine_costs_var = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(1, M))
labor_cost = pulp.lpSum((time_required[0][p] * batches[p] * standard_cost) for p in range(P))
overtime_cost_var = (
    pulp.LpAffineExpression(machine_1_usage - overtime_hour[0]) * overtime_cost
)
overtime_cost_var = pulp.lpSum(max(0, overtime_cost_var))
total_cost = machine_costs_var + labor_cost + overtime_cost_var

profit = revenue - total_cost
problem += profit

# Solve the problem
problem.solve()

# Prepare the output
batches_produced = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')