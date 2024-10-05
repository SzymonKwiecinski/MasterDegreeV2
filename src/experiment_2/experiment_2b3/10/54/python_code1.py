import pulp

# Extracting the data
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]
overtime_hours = pulp.LpVariable('overtime_hours', lowBound=0)

# Objective Function: Total profit
profit_expression = pulp.lpSum(prices[p] * batches[p] for p in range(P))
cost_expression = pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)
) + standard_cost * pulp.lpMin(overtime_hour[0], overtime_hours) + overtime_cost * pulp.lpMax(0, (overtime_hours - overtime_hour[0]))

total_profit = profit_expression - cost_expression

problem += total_profit, "Total Profit"

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Constraint_Machine_{m}"

# No specific availability constraint for machine 1 as per the description
# Overtime constraint for machine 1
problem += pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) - availability[0] <= overtime_hours, "Overtime_Constraint"

# Solve the problem
problem.solve()

# Extracting results
batches_solution = [pulp.value(batches[p]) for p in range(P)]
total_profit_obj = pulp.value(problem.objective)

result = {
    "batches": batches_solution,
    "total_profit": total_profit_obj
}

print(result)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')