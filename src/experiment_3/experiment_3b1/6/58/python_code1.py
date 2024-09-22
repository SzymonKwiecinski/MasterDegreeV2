import pulp
import json

# Input data
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Define indices
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0) for p in range(P)]
setup_flag = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Define the objective function
total_profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
               pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                                                 pulp.lpSum(setup_flag[p] * setup_time[p] for p in range(P))) for m in range(M))

problem += total_profit

# Constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                 pulp.lpSum(setup_flag[p] * setup_time[p] for p in range(P)) <= availability[m], 
                 f'Machine_Availability_Constraint_{m}')

# Non-negativity constraint for batches (already handled by lowBound=0)
# Binary constraint for setup flags (handled by declaring them as binary variables)

# Solve the problem
problem.solve()

# Output results
batches_solution = [pulp.value(batches[p]) for p in range(P)]
setup_flag_solution = [pulp.value(setup_flag[p]) for p in range(P)]
total_profit_value = pulp.value(problem.objective)

print(f'Batches Produced: {batches_solution}')
print(f'Setup Flags: {setup_flag_solution}')
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')