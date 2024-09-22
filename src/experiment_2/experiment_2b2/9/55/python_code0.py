import pulp

# Data from the input
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

# Problem variables
num_machines = len(data['time_required'])
num_parts = len(data['time_required'][0])

# Create the LP Problem
problem = pulp.LpProblem("Auto_Manufacturer_Profit", pulp.LpMaximize)

# Decision Variables: number of batches to produce for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p]) for p in range(num_parts)]

# Objective Function: maximize profit
profit = pulp.lpSum(
    data['prices'][p] * batches[p] for p in range(num_parts)
)

machine_cost = pulp.lpSum(
    data['time_required'][m][p] * batches[p] * data['machine_costs'][m] for m in range(1, num_machines) for p in range(num_parts)
)

# Machine 1 (outsourced, separate handling)
machine_1_cost = (
    pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(num_parts)) * data['standard_cost']
)
machine_1_overtime = (
    pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(num_parts)) - data['overtime_hour']
)
overtime_cost = pulp.lpSum(
    machine_1_overtime * (data['overtime_cost'] - data['standard_cost'])
)

# Total Cost
total_cost = machine_cost + machine_1_cost + overtime_cost

# Profit
total_profit = profit - total_cost
problem += total_profit, "Total_Profit"

# Constraints
# Min profit
problem += total_profit >= data['min_profit']

# Machine usage availability constraint
for m in range(1, num_machines):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(num_parts)) <= data['availability'][m]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "batches": [int(pulp.value(batches[p])) for p in range(num_parts)],
    "total_profit": pulp.value(total_profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')