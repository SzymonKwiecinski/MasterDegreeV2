import pulp

# Parsing the input data
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

# Defining variables for easier access
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# LP Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables: number of batches of each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective Function: Maximize profit
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])

# Costs
machine_cost = []
for m in range(M):
    machine_time = pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)])
    if m == 0:  # Machine 1 with different cost structure
        regular_time = pulp.LpVariable(f'regular_time_{m}', lowBound=0, cat='Continuous')
        overtime = pulp.LpVariable(f'overtime_{m}', lowBound=0, cat='Continuous')
        problem += regular_time + overtime == machine_time
        problem += regular_time <= overtime_hour[m]
        machine_cost.append(
            standard_cost * regular_time + overtime_cost * overtime
        )
    else:
        machine_cost.append(machine_costs[m] * machine_time)

cost = pulp.lpSum(machine_cost)

# Profit is Revenue - Direct Costs
problem += profit - cost

# Constraints
# Machine availability constraints except for machine 1
for m in range(1, M):
    machine_time = pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)])
    problem += machine_time <= availability[m]

# Solve the problem
problem.solve()

# Extracting the results
batches_values = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    'batches': batches_values,
    'total_profit': total_profit
}

print(output)
print(f'(Objective Value): <OBJ>{total_profit}</OBJ>')