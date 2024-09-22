import pulp
import json

# Data
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Constants
P = len(prices)
M = len(machine_costs)

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += profit, "Total_Profit"

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m}"

# Additional constraint for the last two machines
problem += pulp.lpSum(time_required[M-2][p] * batches[p] for p in range(P)) + pulp.lpSum(time_required[M-1][p] * batches[p] for p in range(P)) <= availability[M-1], "Availability_Constraint_M"

# Minimum batches constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_Constraint_{p}"

# Solve the problem
problem.solve()

# Output results
batches_solution = {p: batches[p].varValue for p in range(P)}
total_profit = pulp.value(problem.objective)

print(f'Batches Produced: {batches_solution}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')