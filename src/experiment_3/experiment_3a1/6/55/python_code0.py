import pulp

# Data from the provided JSON
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

# Problem definition
problem = pulp.LpProblem('Maximize_Profit', pulp.LpMaximize)

# Variables
P = len(data['prices'])
b = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Integer')

# Objective Function
total_revenue = pulp.lpSum(data['prices'][p] * b[p] for p in range(P))
total_machine_cost = pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P))) for m in range(len(data['machine_costs'])))
h_1 = pulp.lpSum(data['time_required'][0][p] * b[p] for p in range(P))
overtime_cost = pulp.lpSum(data['standard_cost'] * min(h_1, data['overtime_hour'])) + pulp.lpSum(data['overtime_cost'] * pulp.lpMax(0, h_1 - data['overtime_hour']))

problem += total_revenue - total_machine_cost - overtime_cost, "Total_Profit"

# Constraints
# Production Constraints
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"MinBatches_Constraint_{p}"

# Machine Availability Constraints
for m in range(len(data['availability'])):
    problem += pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) <= data['availability'][m], f"Availability_Constraint_{m}"

# Total Hour Constraints for Machine 1
problem += h_1 <= data['availability'][0], "Total_Hour_Constraint_1"

# Profit Constraint
problem += total_revenue - total_machine_cost - overtime_cost >= data['min_profit'], "Profit_Constraint"

# Solve the problem
problem.solve()

# Outputs
batches = [b[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches produced: {batches}')
print(f'Total Profit: <OBJ>{total_profit}</OBJ>')