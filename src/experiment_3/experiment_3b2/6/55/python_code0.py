import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

# Define the sets
P = range(len(data['prices']))  # Parts
M = range(len(data['machine_costs']))  # Machines

# Define the problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", P, lowBound=0, cat='Continuous')

# Objective Function
total_profit = pulp.lpSum(data['prices'][p] * batches[p] for p in P) - \
               pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) for m in M) - \
               pulp.lpSum(data['time_required'][1][p] * batches[p] for p in P) * data['standard_cost'] if pulp.lpSum(data['time_required'][1][p] * batches[p] for p in P) <= data['overtime_hour'] else \
               (data['overtime_hour'] * data['standard_cost'] + 
                (pulp.lpSum(data['time_required'][1][p] * batches[p] for p in P) - data['overtime_hour']) * data['overtime_cost'])

problem += total_profit, "Objective"

# Constraints
# Machine Time Availability for machines 2 and 3
for m in range(1, len(data['machine_costs'])):  # skipping machine 1
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) <= data['availability'][m], f"MachineAvailability_{m}"

# Minimum Batch Requirement
for p in P:
    problem += batches[p] >= data['min_batches'][p], f"MinBatches_{p}"

# Minimum Profit Requirement
problem += total_profit >= data['min_profit'], "MinProfit"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')