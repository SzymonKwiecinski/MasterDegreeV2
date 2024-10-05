import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'extra_costs': [0, 15, 22.5], 
    'max_extra': [0, 80, 80]
}

# Indices
P = len(data['prices'])  # Number of parts
M = len(data['availability'])  # Number of machines

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=data['min_batches'][p]) for p in range(P)]
e = [pulp.LpVariable(f'e_{m}', lowBound=0, upBound=data['max_extra'][m]) for m in range(M)]

# Objective Function
profit_terms = [data['prices'][p] * x[p] for p in range(P)]
cost_terms = [data['time_required'][m][p] * x[p] * data['machine_costs'][m] for m in range(M) for p in range(P)]
extra_hours_costs = [e[m] * data['extra_costs'][m] for m in range(M)]

problem += pulp.lpSum(profit_terms) - (pulp.lpSum(cost_terms) + pulp.lpSum(extra_hours_costs))

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m], f"Machine_{m}_time_availability"

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')