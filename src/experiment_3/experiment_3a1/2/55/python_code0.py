import pulp

# Data extracted from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'standard_cost': 20, 
    'overtime_cost': 30, 
    'overtime_hour': 400, 
    'min_profit': 5000
}

# Extract parameters
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

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective Function
# Labor cost calculation
hours_used_1 = pulp.lpSum(time_required[0][p] * b[p] for p in range(P))
labor_cost = pulp.LpVariable("labor_cost")

problem += (pulp.lpSum(prices[p] * b[p] for p in range(P)) 
             - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) for m in range(M))
             - labor_cost, "Total_Profit")

# Constraints for labor cost
problem += labor_cost == (
    standard_cost * hours_used_1 if hours_used_1 <= overtime_hour 
    else (standard_cost * overtime_hour + overtime_cost * (hours_used_1 - overtime_hour))
)

# Availability constraints for each machine
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m+1}")

# Minimum production requirements for each part
for p in range(P):
    problem += (b[p] >= min_batches[p], f"Min_Batches_Constraint_{p+1}")

# Profit requirement constraint
total_profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) for m in range(M)) - labor_cost
problem += (total_profit >= min_profit, "Profit_Requirement")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')