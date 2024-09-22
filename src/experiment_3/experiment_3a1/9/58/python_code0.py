import pulp
import json

# Data from the provided JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Parameters
P = len(data['prices'])  # Number of different parts
M = len(data['machine_costs'])  # Number of different machines
time_required = data['time_required']  # time[m][p]
machine_costs = data['machine_costs']  # cost[m]
availability = data['availability']  # available[m]
prices = data['prices']  # price[p]
setup_time = data['setup_time']  # setup_time[p]

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Create the Problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m}"

# Setup time constraint for machine 1 (index 0)
problem += pulp.lpSum(setup_flags[p] for p in range(P)) >= \
           pulp.lpSum(setup_flags[p] * setup_time[p] for p in range(P)), "Setup_Time_Constraint"

# Solve the Problem
problem.solve()

# Output results
batches_solution = {p: pulp.value(batches[p]) for p in range(P)}
setup_flags_solution = {p: pulp.value(setup_flags[p]) for p in range(P)}
total_profit = pulp.value(problem.objective)

print(f'Batches produced for each part: {batches_solution}')
print(f'Setup flags for each part: {setup_flags_solution}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')