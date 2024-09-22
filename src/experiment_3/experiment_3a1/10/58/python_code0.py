import pulp
import json

data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Extracting data
time_required = data['time_required']  # time_{m,p}
machine_costs = data['machine_costs']  # cost_{m}
availability = data['availability']      # available_{m}
prices = data['prices']                  # price_{p}
setup_time = data['setup_time']          # setup_time_{p}

P = len(prices)    # Number of different parts
M = len(machine_costs)  # Number of different machines

# Create model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective Function
total_profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * (
    pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
    pulp.lpSum(setup_flags[p] * setup_time[p] * (1 if m == 0 else 0) for p in range(P))
) for m in range(M))

problem += total_profit

# Constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                 pulp.lpSum(setup_flags[p] * setup_time[p] * (1 if m == 0 else 0) for p in range(P))
                 <= availability[m], f"Availability_Constraint_{m}")

# Solve the problem
problem.solve()

# Output results
batches_result = [pulp.value(batches[p]) for p in range(P)]
setup_flags_result = [pulp.value(setup_flags[p]) for p in range(P)]
total_profit_value = pulp.value(problem.objective)

print(f'batches: {batches_result}')
print(f'setup_flags: {setup_flags_result}')
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')