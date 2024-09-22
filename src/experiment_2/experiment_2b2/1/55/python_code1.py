import pulp

# Input data
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

P = len(data['prices'])
M = len(data['machine_costs'])

# Initialize the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

# Constraints for machines other than machine 1
for m in range(1, M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Revenue calculation
revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))

# Machine 1 cost calculation
machine_1_hours = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))
overtime_hours = pulp.LpVariable('overtime_hours', lowBound=0, cat='Continuous')
problem += overtime_hours >= machine_1_hours - data['overtime_hour']
problem += overtime_hours >= 0

# Calculate cost for machine 1 considering both standard and overtime hours
machine_1_cost = (data['standard_cost'] * (machine_1_hours - overtime_hours) + 
                  data['overtime_cost'] * overtime_hours)

# Machine costs calculation excluding machine 1
machine_costs = machine_1_cost
for m in range(1, M):
    machine_costs += data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P))

# Profit calculation
profit = revenue - machine_costs

# Objective
problem += profit

# Profit constraint
problem += profit >= data['min_profit']

# Solve the problem
problem.solve()

# Output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')