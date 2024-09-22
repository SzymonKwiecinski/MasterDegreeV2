import pulp
import json

# Load data from the provided JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

# Constants
P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

# Objective Function
problem += pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + extra_costs[m] * extra_time[m] for m in range(M))

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] + extra_time[m], f"Machine_Time_Constraint_{m}"

for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batch_Constraint_{p}"

for m in range(M):
    problem += extra_time[m] <= max_extra[m], f"Max_Extra_Time_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')