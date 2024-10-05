import pulp

# Load input data
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
num_machines = data['NumMachines']
num_parts = data['NumParts']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create decision variables for number of batches
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(num_parts)]

# Objective function: Maximize profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts))
cost = (
    pulp.lpSum(
        time_required[m][p] * batches[p] * machine_costs[m] for m in range(1, num_machines) for p in range(num_parts)
    ) +
    pulp.lpSum(
        # Special case for Machine 1 (index 0)
        pulp.lpSum(
            time_required[0][p] * batches[p] 
            * (standard_cost if pulp.lpSum(time_required[0][p] * batches[p]) <= overtime_hour[0] else overtime_cost)
            for p in range(num_parts)
        )
    )
)
problem += profit - cost

# Constraints
# Machine time availability constraints
for m in range(1, num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m]

# Solve problem
problem.solve()

# Extract results
batches_produced = [pulp.value(batches[p]) for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

# Output result formatted as specified
output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')