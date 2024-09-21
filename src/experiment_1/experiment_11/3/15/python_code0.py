import pulp

# Data from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Defining parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create a problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

# Constraints
# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m], f"Machine_Availability_{m}"

# Minimum production requirement
for p in range(P):
    problem += x[p] >= data['min_batches'][p], f"Min_Production_{p}"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')