import pulp
import json

# Data in JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extract data
time_required = data['time_required']  # time_required[m][p]
machine_costs = data['machine_costs']  # cost_m
availability = data['availability']      # available_m
prices = data['prices']                  # price_p
min_batches = data['min_batches']        # min_batches_p

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Decision Variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m+1}"

# Shared Availability Constraint for last two machines
problem += pulp.lpSum(time_required[M-1][p] * b[p] for p in range(P)) + \
           pulp.lpSum(time_required[M-2][p] * b[p] for p in range(P)) <= \
           availability[M-1] + availability[M-2], "Shared_Availability_Constraint"

# Minimum Production Requirements
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Production_Requirement_{p+1}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')