import pulp

# Data extraction from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Define parameters
P = len(data['prices'])  # Number of different parts
M = len(data['machine_costs'])  # Number of different machines

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective function
profit_terms = [data['prices'][p] * batches[p] for p in range(P)]
cost_terms = [data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M)]
problem += pulp.lpSum(profit_terms) - pulp.lpSum(cost_terms), "Total_Profit"

# Constraints
# Minimum batches produced for each part
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}"

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Machine_Availability_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')