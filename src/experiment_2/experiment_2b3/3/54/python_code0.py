import pulp

# Load the data
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

# Extract data
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

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
batches = [pulp.LpVariable(f'batches_{p}', min_batches[p], cat='Continuous') for p in range(P)]
machine_hours = [pulp.LpVariable(f'machine_hours_{m}', 0, cat='Continuous') for m in range(M)]
overtime_hours = [pulp.LpVariable(f'overtime_hours_{m}', 0, cat='Continuous') for m in range(1)]

# Objective function
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = (pulp.lpSum(machine_costs[m] * machine_hours[m] for m in range(1, M)) +
         pulp.lpSum(standard_cost * machine_hours[0] + overtime_cost * overtime_hours[0]))
profit = revenue - costs
problem += profit

# Constraints
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= machine_hours[m]
    problem += machine_hours[m] <= availability[m]

# Special constraints for outsourced machine (Machine 1)
problem += machine_hours[0] == pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
problem += machine_hours[0] <= overtime_hour[0] + overtime_hours[0]
problem += overtime_hours[0] >= 0

# Solve
problem.solve()

# Output results
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(output)