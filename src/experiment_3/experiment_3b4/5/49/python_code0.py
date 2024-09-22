import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{p}", lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
revenue = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))
costs = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M))
profit = revenue - costs
problem += profit

# Constraints

# Machine Availability Constraints
for m in range(M-2):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Shared Availability for Machines M-1 and M
problem += (
    pulp.lpSum(data['time_required'][M-2][p] * x[p] for p in range(P)) +
    pulp.lpSum(data['time_required'][M-1][p] * x[p] for p in range(P))
    <= data['availability'][M-2] + data['availability'][M-1]
)

# Minimum Production Requirement
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Solve the problem
problem.solve()

# Print the results
for p in range(P):
    print(f"Batches of part {p+1} produced: {x[p].varValue}")
    
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")