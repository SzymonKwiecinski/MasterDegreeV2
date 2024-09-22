import pulp

# Data from the provided JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Constants
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M))
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Last two machines combined constraint
if M > 1:
    problem += pulp.lpSum(data['time_required'][M - 1][p] * x[p] for p in range(P)) + \
                pulp.lpSum(data['time_required'][M - 2][p] * x[p] for p in range(P)) <= data['availability'][M - 1] + data['availability'][M - 2]

# Minimum batches constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')