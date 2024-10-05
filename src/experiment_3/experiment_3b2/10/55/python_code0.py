import pulp
import json

# Load data from the JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision variables
P = len(data['prices'])
x = pulp.LpVariable.dicts("batch", range(P), lowBound=0, cat='Integer')

# Parameters
prices = data['prices']
min_batches = data['min_batches']
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']

# Objective function: total profit
total_profit = pulp.lpSum([prices[p] * x[p] for p in range(P)]) - \
               pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) for m in range(1, len(machine_costs))]) 

# Labor cost for machine 1
y_1 = pulp.lpSum([time_required[0][p] * x[p] for p in range(P)])
labor_cost = pulp.LpVariable("Labor_Cost")

# Define labor cost constraints
problem += labor_cost == pulp.lpIf(y_1 <= overtime_hour, y_1 * standard_cost, 
                                    overtime_hour * standard_cost + (y_1 - overtime_hour) * overtime_cost)

# Adding constraints
# Machine Time Availability
for m in range(1, len(machine_costs)):
    problem += pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) <= availability[m]

# Minimum Production Requirement
for p in range(P):
    problem += x[p] >= min_batches[p]

# Profit Constraint
problem += total_profit >= data['min_profit']

# Set objective
problem += total_profit

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')