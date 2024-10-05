from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Extract input data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

M = len(time_required)  # number of machines
P = len(prices)  # number of parts

# Create problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Decision variables
batches = LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')
setup_flags = LpVariable.dicts("Setup", range(P), lowBound=0, upBound=1, cat='Binary')

# Objective function
profit = lpSum(prices[p] * batches[p] for p in range(P)) - lpSum(
    machine_costs[m] * (lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
    setup_flags[0] * setup_time[p]) for m in range(M)
)
problem += profit

# Constraints
for m in range(M):
    problem += lpSum(time_required[m][p] * batches[p] for p in range(P)) + (setup_flags[0] * setup_time[p] if m == 0 else 0) <= availability[m]

# Solve the problem
problem.solve()

# Get results
batches_result = [batches[p].varValue for p in range(P)]
setup_flags_result = [setup_flags[p].varValue for p in range(P)]
total_profit = value(problem.objective)

# Output result
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}
print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')