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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Sets
P = len(data['prices'])
M = len(data['machine_costs'])

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
overtime_h = pulp.LpVariable("overtime_h", lowBound=0, cat='Continuous')

# Objective Function
T1 = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))
C1 = data['standard_cost'] * (T1 - data['overtime_hour']) + data['overtime_cost'] * overtime_h
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M)) - C1
problem += profit, "Total_Profit"

# Constraints
# Availability constraints for machines m = 2, ..., M
for m in range(1, M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Availability_Constraint_Machine_{m+1}"

# Minimum batches produced
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Minimum_Batches_Constraint_{p+1}"

# Overtime condition for machine 1
problem += overtime_h == pulp.lpMax(0, T1 - data['overtime_hour']), "Overtime_Condition"

# Profit constraint
problem += profit >= data['min_profit'], "Profit_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')