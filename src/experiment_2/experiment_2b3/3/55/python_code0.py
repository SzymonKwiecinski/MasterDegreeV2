import pulp

# The given data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}

# Variables for data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: batches produced for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Additional decision variables for machine 1's time usage
machine_1_standard_time = pulp.LpVariable('machine_1_standard_time', lowBound=0, cat='Continuous')
machine_1_overtime = pulp.LpVariable('machine_1_overtime', lowBound=0, cat='Continuous')

# Objective function: Maximize profit
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = 0

# Calculate costs for each machine
for m in range(M):
    if m == 0:
        # Special handling for machine 1
        costs += (standard_cost * machine_1_standard_time + overtime_cost * machine_1_overtime)
    else:
        costs += machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P))

profit = revenue - costs
problem += profit

# Constraints
# Machine 1 specific constraints
problem += machine_1_standard_time + machine_1_overtime == pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
problem += machine_1_standard_time <= overtime_hour

# Standard availability constraints for other machines
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Minimum profit constraint
problem += profit >= min_profit

# Solve the problem
problem.solve()

# Output the result
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')