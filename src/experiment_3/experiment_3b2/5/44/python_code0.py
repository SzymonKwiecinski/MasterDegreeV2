import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define variables
P = len(data['prices'])
M = len(data['machine_costs'])

# Decision variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=10)  # Starting at minimum batches

# Objective function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - \
         pulp.lpSum((pulp.lpSum(data['time_required[m][p]'] * x[p] for p in range(P))) * data['machine_costs'][m] for m in range(M))

problem += profit

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Non-negativity constraints are implicitly handled by lower bound in variable definition.

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')