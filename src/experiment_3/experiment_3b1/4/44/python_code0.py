import pulp
import json

# Data from the provided JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])  # Number of different parts
M = len(data['machine_costs'])  # Number of different machines
time_required = data['time_required']  # time_m,p
machine_costs = data['machine_costs']  # cost_m
availability = data['availability']  # available_m
prices = data['prices']  # price_p
min_batches = data['min_batches']  # min_batches_p

# Initialize the problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += profit, "Total_Profit"

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m}"

# Constraints for minimum production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Minimum_Batches_{p}"

# Solve the problem
problem.solve()

# Output results
batches_produced = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches Produced: {batches_produced}')
print(f'Total Profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')