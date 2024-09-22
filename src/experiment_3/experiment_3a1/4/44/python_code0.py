import pulp

# Data from the JSON input
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Defining the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Indices
P = len(data['min_batches'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
cost = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))
problem += profit - cost

# Constraints: Machine Availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Machine_Availability_{m}"

# Constraints: Minimum Production Requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Production_{p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')