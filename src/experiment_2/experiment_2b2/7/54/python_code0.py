import pulp

# Data from JSON
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

# Unpacking data
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

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f'Batches_{p}', lowBound=min_batches[p]) for p in range(P)]
machine_1_hours = pulp.LpVariable('Machine_1_Hours', lowBound=0)

# Objective
profit = pulp.lpSum(
    [batches[p] * (prices[p] - pulp.lpSum(time_required[m][p] * machine_costs[m] for m in range(M)))
     for p in range(P)]
)

# Consider outsourced machine 1
profit -= machine_1_hours * standard_cost
profit -= (pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) - machine_1_hours) * (overtime_cost - standard_cost)
problem += profit

# Constraining the machine hours except for Machine 1
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Machine 1 constraints
problem += machine_1_hours <= overtime_hour[0]
problem += pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) <= machine_1_hours + overtime_hour[0]

# Solve
problem.solve()

# Output
num_batches = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": num_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')