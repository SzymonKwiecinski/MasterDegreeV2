import pulp

# Data from the provided JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Define sets
P = range(len(data['prices']))  # set of parts
M = range(len(data['machine_costs']))  # set of machines

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", P, lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in P) - \
         pulp.lpSum(data['machine_costs'][m] * 
                     pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) 
                     for m in M)

problem += profit, "Total_Profit"

# Constraints
for m in M:
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) <= data['availability'][m], f"Machine_Availability_{m}"

for p in P:
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')