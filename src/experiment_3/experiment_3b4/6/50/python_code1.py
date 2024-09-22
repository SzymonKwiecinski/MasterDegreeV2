import pulp

# Data from the JSON
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
P = len(data['prices'])  # Number of products
M = len(data['availability'])  # Number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]
e = [pulp.LpVariable(f'e_{m}', lowBound=0, upBound=data['max_extra'][m], cat='Continuous') for m in range(M)]

# Objective function
profit = (
    pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) -
    pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) 
                                            + data['extra_costs'][m] * e[m]) for m in range(M))
)
problem += profit

# Machine time constraints
for m in range(M):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m],
        f"Machine_Time_Constraint_{m}"
    )

# Minimum production constraints
for p in range(P):
    problem += (x[p] >= data['min_batches'][p], f"Min_Production_Constraint_{p}")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')