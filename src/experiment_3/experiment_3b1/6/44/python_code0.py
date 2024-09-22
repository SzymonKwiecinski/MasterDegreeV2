import pulp
import json

data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Define parameters
time_required = data['time_required']  # time_required[m][p]
machine_costs = data['machine_costs']  # cost_m
availability = data['availability']  # available_m
prices = data['prices']  # price_p
min_batches = data['min_batches']  # min_batches_p

P = len(prices)  # number of parts
M = len(availability)  # number of machines

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

# Constraints
# Machine time availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m}"

# Minimum batches produced constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Output the results
for p in range(P):
    print(f'Batches for part {p+1}: {batches[p].varValue}')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')