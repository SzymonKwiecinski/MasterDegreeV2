import pulp
import json

# Load data
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')  # batches produced for part p
y = pulp.LpVariable.dicts("y", range(M), lowBound=0, upBound=max_extra, cat='Continuous')  # extra hours purchased for machine m

# Objective Function
problem += pulp.lpSum(prices[p] * x[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * (availability[m] + y[m]) for m in range(M)) - \
           pulp.lpSum(extra_costs[m] * y[m] for m in range(M)), "Total Profit"

# Constraints
# Time constraints for each machine
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m] + y[m], f"Machine_{m+1}_Time_Constraint"

# Minimum production requirements
for p in range(P):
    problem += x[p] >= min_batches[p], f"Min_Batches_Required_for_Part_{p+1}"

# Non-negativity constraints are already defined by default

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')