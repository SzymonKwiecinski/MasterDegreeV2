import pulp
import json

# Load data from JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Define the parameters based on the input data
time_required = data['time_required']  # time[m][p]
machine_costs = data['machine_costs']  # cost[m]
availability = data['availability']      # available[m]
prices = data['prices']                  # price[p]
setup_time = data['setup_time']          # setup_time[p]

# Number of parts and machines
P = len(prices)      # Number of parts
M = len(machine_costs)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Define decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function
profit_expr = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
              pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit_expr, "Total_Profit"

# Constraints
# Machine 1 constraint (includes setup time)
problem += (pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) +
             pulp.lpSum(setup_flags[p] * setup_time[p] for p in range(P))) <= availability[0], "Machine_1_Availability")

# Other machine constraints
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_{m+1}_Availability"

# Setup flags and batches constraints
for p in range(P):
    problem += batches[p] >= 0, f"Batches_NonNegativity_{p+1}"
    problem += setup_flags[p] >= 0, f"SetupFlags_0_1_{p+1}"
    problem += setup_flags[p] <= 1, f"SetupFlags_0_1_Upper_{p+1}"

# Solve the problem
problem.solve()

# Output results
batches_result = [batches[p].varValue for p in range(P)]
setup_flags_result = [setup_flags[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches: {batches_result}')
print(f'Setup Flags: {setup_flags_result}')
print(f'Total Profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')