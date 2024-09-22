import pulp
import json

# Load data from JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

P = len(prices)    # Number of different parts
M = len(machine_costs)  # Number of different machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)
)
problem += profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (
        pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
        pulp.lpSum(setup_flags[p] * setup_time[p] for p in range(P)) <= availability[m]
    )

# Setup time for part p on machine 1
for p in range(P):
    problem += setup_flags[p] <= 1

# Solve the problem
problem.solve()

# Output results
batches_result = {f'part_{p}': pulp.value(batches[p]) for p in range(P)}
setup_flags_result = {f'part_{p}': pulp.value(setup_flags[p]) for p in range(P)}
total_profit = pulp.value(problem.objective)

print(batches_result)
print(setup_flags_result)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')