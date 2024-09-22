import pulp
import json

# Data input
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}")

# Parameters
P = len(data['setup_time'])
M = len(data['time_required'])

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - pulp.lpSum([machine_costs[m] * (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) + (setup_flags[p] * setup_time[p] if m == 0 else 0)) for m in range(M)])
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_Constraint_m{m}"

problem += setup_flags[0] * setup_time[0] + pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)]) <= availability[0], "Setup_Time_Constraint_m1"

# Solve the problem
problem.solve()

# Output results
batches_result = {f'batches_{p}': batches[p].varValue for p in range(P)}
setup_flags_result = {f'setup_flag_{p}': setup_flags[p].varValue for p in range(P)}
total_profit = pulp.value(problem.objective)

print(batches_result)
print(setup_flags_result)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')