import pulp

# Data
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

# Unpack the data
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour'][0]  # Use overtime_hour for machine 1

# LP Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p+1}', lowBound=min_batches[p]) for p in range(P)]

# Objective function
revenue = pulp.lpSum(prices[p] * x[p] for p in range(P))
machine_costs_total = pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P))
    for m in range(1, M)
)

machine_1_usage = pulp.lpSum(time_required[0][p] * x[p] for p in range(P))
labor_costs = standard_cost * pulp.lpSum(
    pulp.lpMin(overtime_hour, machine_1_usage)
)

overtime_costs = overtime_cost * (
    machine_1_usage - overtime_hour
)
overtime_costs = pulp.lpMax(0, overtime_costs)

total_profit = revenue - machine_costs_total - labor_costs - overtime_costs
problem += total_profit

# Constraints
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')