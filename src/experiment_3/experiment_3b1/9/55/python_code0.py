import pulp
import json

# Data provided in JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')
    
# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

P = len(prices)  # Number of parts
M = len(availability)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)
)
problem += profit, "Total_Profit"

# Constraints

# Machine availability constraints
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m+1}"

# Minimum batch production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batch_Prod_{p+1}"

# Machine 1 labor cost constraint
total_time_m1 = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
overtime_cost_constraint = standard_cost * pulp.lpMin(total_time_m1, overtime_hour) + \
                           (total_time_m1 - overtime_hour) * overtime_cost
problem += total_time_m1 <= availability[0] + (overtime_cost_constraint if total_time_m1 > availability[0] else 0), "Machine_1_Constraint"

# Overall profit constraint
problem += profit >= min_profit, "Min_Profit_Constraint"

# Solve the problem
problem.solve()

# Output the results
batches_solution = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches produced: {batches_solution}')
print(f'Total profit: {total_profit}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')