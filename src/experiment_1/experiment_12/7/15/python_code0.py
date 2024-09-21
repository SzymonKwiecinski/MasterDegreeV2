import pulp

# Data extracted from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Parameters
num_parts = len(data['prices'])
num_machines = len(data['machine_costs'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(num_parts)]

# Objective Function
profit = pulp.lpSum([data['prices'][p] * x[p] for p in range(num_parts)])
costs = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(num_parts)]) for m in range(num_machines)])
problem += profit - costs, "Profit"

# Constraints
# Non-negativity and minimum production constraint
for p in range(num_parts):
    problem += x[p] >= data['min_batches'][p], f"MinBatches_{p}"

# Machine availability constraints
for m in range(num_machines):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(num_parts)]) <= data['availability'][m], f"Availability_{m}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')