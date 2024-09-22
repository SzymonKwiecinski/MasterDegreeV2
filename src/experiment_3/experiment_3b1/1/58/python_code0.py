import pulp
import json

# Data from the provided JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Parameters
time_required = data['time_required']  # Machine time required for each part
machine_costs = data['machine_costs']  # Cost per hour for each machine
availability = data['availability']      # Available hours per month for each machine
prices = data['prices']                  # Selling price per batch of part
setup_time = data['setup_time']          # Setup time for each part

P = len(prices)     # Number of different parts
M = len(machine_costs)  # Number of different machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += profit

# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m])

# Setup time constraint for machine 1
problem += (pulp.lpSum([setup_flags[p] * setup_time[p] for p in range(P)]) <= availability[0])

# Solve the problem
problem.solve()

# Output results
batches_solution = [batches[p].varValue for p in range(P)]
setup_flags_solution = [setup_flags[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches produced: {batches_solution}')
print(f'Setup flags: {setup_flags_solution}')
print(f'Total Profit: <OBJ>{total_profit}</OBJ>')