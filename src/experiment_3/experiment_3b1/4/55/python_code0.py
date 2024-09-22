import pulp
import json

# Data from the JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Constants
P = len(prices)  # Number of parts
M = len(time_required)  # Number of machines

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)  # batches produced for parts

# Objective Function
total_profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - pulp.lpSum(
    machine_costs[m] * (pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) if pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) <= overtime_hour else
    (standard_cost * overtime_hour + overtime_cost * (pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) - overtime_hour))) 
    for m in range(M)
)

# Adding the objective function to the problem
problem += total_profit, "Total_Profit"

# Constraints
# Production requirements
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Batches_Requirement_for_part_{p}"

# Machine hours availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) <= availability[m], f"Machine_{m+1}_Availability"

# Profit condition
problem += total_profit >= min_profit, "Min_Profit_Condition"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')