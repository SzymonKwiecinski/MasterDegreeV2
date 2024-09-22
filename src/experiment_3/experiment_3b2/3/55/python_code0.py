import pulp
import json

# Data input
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['availability'])  # Number of machines
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

# Objective function
labor_cost = pulp.LpVariable("LaborCost")
profit = pulp.lpSum(prices[p] * x[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(1, M)) - labor_cost

problem += profit

# Labor cost constraints
total_time = pulp.lpSum(time_required[0][p] * x[p] for p in range(P))
problem += labor_cost == (standard_cost * total_time if total_time <= overtime_hour else 
                           standard_cost * overtime_hour + 
                           overtime_cost * (total_time - overtime_hour))

# Constraints
for p in range(P):
    problem += x[p] >= min_batches[p], f"Min_batches_constraint_part_{p}"

for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m], f"Availability_constraint_machine_{m}"

problem += profit >= min_profit, "Profit_constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')