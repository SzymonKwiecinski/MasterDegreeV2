import pulp
import json

# Load data from the provided JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')

# Extracting data for easier use
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
M = len(machine_costs)  # Number of machines

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Continuous')

# Define the objective function
hours_used = [pulp.lpSum((time_required[m][p] / 100) * b[p] for p in range(P)) for m in range(M)]
labor_cost = pulp.lpSum([standard_cost * hours_used[0] if hours_used[0] <= overtime_hour else 
                          standard_cost * overtime_hour + overtime_cost * (hours_used[0] - overtime_hour)])
                        
profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * hours_used[m] for m in range(M)) - labor_cost
problem += profit, "Total_Profit"

# Constraints
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Batches_Constraint_{p+1}"

for m in range(M):
    problem += pulp.lpSum((time_required[m][p] / 100) * b[p] for p in range(P)) <= availability[m], f"Machine_Availability_Constraint_{m+1}"

problem += profit >= min_profit, "Min_Profit_Constraint"

# Solve the problem
problem.solve()

# Print results
for p in range(P):
    print(f'Batches produced for part {p+1}: {b[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')