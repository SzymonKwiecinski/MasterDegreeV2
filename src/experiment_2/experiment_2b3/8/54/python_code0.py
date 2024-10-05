import pulp

# Input data
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

# Parameters
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

# Define LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for number of batches of each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Decision variable for hours on machine 1
hours_machine1 = pulp.LpVariable('hours_machine1', lowBound=0, cat='Continuous')

# Objective function: Maximize profit
revenue = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
machine_costs_total = pulp.lpSum([time_required[m][p] * batches[p] * machine_costs[m] for m in range(1, M) for p in range(P)])
standard_costs = standard_cost * hours_machine1
overtime_costs = overtime_cost * (hours_machine1 - overtime_hour[0])

problem += revenue - machine_costs_total - standard_costs - pulp.lpSum([pulp.max_(0, hours_machine1 - overtime_hour[0]) * (overtime_cost - standard_cost)])

# Constraints

for m in range(1, M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Machine 1 usage constraint
problem += hours_machine1 == pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)])

# Solve problem
problem.solve()

# Gather results
batches_result = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')