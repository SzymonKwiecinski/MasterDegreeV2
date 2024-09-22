import pulp
import json

# Data input
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Parameters
P = len(data['prices'])
M = len(data['machine_costs'])
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, upBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("AutoPartsMaxProfit", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * (availability[m] + extra_time[m]) for m in range(M)) - \
           pulp.lpSum(extra_costs[m] * extra_time[m] for m in range(M))

# Constraints
# Machine Time Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] + extra_time[m]

# Minimum Batches Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Output
batches_output = [batches[p].varValue for p in range(P)]
extra_time_output = [extra_time[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

print(f'Batches Produced: {batches_output}')
print(f'Extra Time Purchased: {extra_time_output}')
print(f'Total Profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')