import pulp

# Data
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{p}", lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
profit = (
    pulp.lpSum(prices[p] * x[p] for p in range(P)) -
    pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M))
)
problem += profit

# Constraints
# Non-negativity and Minimum production requirements
for p in range(P):
    problem += x[p] >= min_batches[p]

# Machine time availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

# Solve
problem.solve()

# Output
print("Status:", pulp.LpStatus[problem.status])
for p in range(P):
    print(f"Number of batches of part {p+1}: {x[p].varValue}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")