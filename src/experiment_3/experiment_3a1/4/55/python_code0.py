import pulp

# Data from the provided JSON format
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

# Problem setup
problem = pulp.LpProblem("Auto_Parts_Manufacturer_Problem", pulp.LpMaximize)

# Number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Decision variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)  # batches produced for each part

# Objective function
profit = pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) for m in range(M))

# Adding labor costs for machine 1
labor_cost_machine_1 = pulp.lpSum(data['standard_cost'] * pulp.lpMin(pulp.lpSum(data['time_required'][0][p] * b[p] for p in range(P)), data['overtime_hour']) + 
                                 data['overtime_cost'] * pulp.lpMax(0, pulp.lpSum(data['time_required'][0][p] * b[p] for p in range(P)) - data['overtime_hour']))

# Final objective function including labor costs for machine 1
problem += profit - labor_cost_machine_1

# Constraints
# Time availability for each machine
for m in range(M):
    problem += pulp.lpSum(data['time_required[m][p]'] * b[p] for p in range(P)) <= data['availability'][m], f"Time_Availability_Machine_{m}"

# Minimum batch requirements
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Min_Batches_Part_{p}"

# Profit constraint
problem += profit >= data['min_profit'], "Min_Profit"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')