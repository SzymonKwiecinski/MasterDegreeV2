import pulp

# Extract the data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

M = len(time_required)  # number of machines
P = len(prices)         # number of parts

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches of each part to produce
batches = [pulp.LpVariable(f"batches_{p+1}", lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function: maximize profit
# Profit = Revenue - Cost
# Revenue from selling parts = sum(prices[p] * batches[p] for p)
# Cost of machine usage = sum(costs[m] * sum(time_required[m][p] * batches[p] for p) for m)
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += revenue - cost, "Total_Profit"

# Constraints: machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_{m+1}_Availability"

# Solve the problem
problem.solve()

# Extract the results
batches_produced = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')