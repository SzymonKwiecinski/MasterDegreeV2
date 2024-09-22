import pulp

# Parse the JSON data
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

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batch_{p+1}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Define objective function
profit = sum(prices[p] * batches[p] for p in range(P))
machine_cost = sum(machine_costs[m] * time_required[m][p] * batches[p] for p in range(P) for m in range(1, M))

# Correct labor cost calculation using additional decision variable for effective hours
regular_hours = [pulp.LpVariable(f'regular_hours_{p+1}', lowBound=0, upBound=overtime_hour[0], cat='Continuous') for p in range(P)]
overtime_hours = [pulp.LpVariable(f'overtime_hours_{p+1}', lowBound=0, cat='Continuous') for p in range(P)]

for p in range(P):
    problem += (regular_hours[p] + overtime_hours[p] == time_required[0][p] * batches[p])

labor_cost = sum(standard_cost * regular_hours[p] + overtime_cost * overtime_hours[p] for p in range(P))

total_profit = profit - machine_cost - labor_cost
problem += total_profit

# Add constraints
for m in range(1, M):  # Machine m, m=1 is the outsourced machine
    problem += sum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Get results
batches_result = [pulp.value(batches[p]) for p in range(P)]
total_profit_value = pulp.value(problem.objective)

# Print outputs
output = {
    "batches": batches_result,
    "total_profit": total_profit_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')