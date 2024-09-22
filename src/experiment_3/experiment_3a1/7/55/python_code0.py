import pulp
import json

# Input data in JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Define sets
P = len(prices)  # Number of different parts
M = len(machine_costs)  # Number of different machines

# Create the problem variable
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Labor cost calculation as a function of batches
def labor_cost():
    total_time = sum(time_required[m][p] * batches[p] for p in range(P) for m in range(M))
    if total_time <= overtime_hour:
        return standard_cost * total_time
    else:
        return (standard_cost * overtime_hour) + (overtime_cost * (total_time - overtime_hour))

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)) - \
         labor_cost()

problem += profit, "Total_Profit"

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m}"

for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batch_Constraint_{p}"

problem += profit >= min_profit, "Min_Profit_Constraint"

# Solve the problem
problem.solve()

# Print result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')