import pulp
import json

# Data from the provided JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Unpacking data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Sets
parts = range(len(prices))
machines = range(len(machine_costs))

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", parts, lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("SetupFlag", parts, cat='Binary')

# Objective Function
profit = (
    pulp.lpSum(prices[p] * batches[p] for p in parts) -
    pulp.lpSum(machine_costs[m] * time_required[m][p] * batches[p] for m in machines for p in parts) -
    pulp.lpSum(machine_costs[0] * setup_time[p] * setup_flag[p] for p in parts)
)
problem += profit

# Constraints
# Machine availability constraints
for m in machines:
    problem += (
        pulp.lpSum(time_required[m][p] * batches[p] for p in parts) +
        (pulp.lpSum(setup_time[p] * setup_flag[p] for p in parts) if m == 0 else 0) <= availability[m]
    )

# Setup flags constraint for machine 1
for p in parts:
    problem += batches[p] <= len(machines) * setup_flag[p]

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')