import pulp
import json

# Data from the provided JSON format
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

# Defining number of parts (P) and machines (M)
P = len(prices)
M = len(machine_costs)

# Creating problem
problem = pulp.LpProblem("AutoParts_Manufacturing", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
H1 = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))  # Total hours on machine 1

# Labor costs calculation with conditions
labor_costs = (
    standard_cost * H1 if H1 <= overtime_hour 
    else standard_cost * overtime_hour + overtime_cost * (H1 - overtime_hour)
)

# Total profit calculation
total_profit = profit - costs - labor_costs
problem += total_profit, "Total_Profit"

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m+1}"

# Minimum production constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_Constraint_{p+1}"

# Profit constraint
problem += total_profit >= min_profit, "Min_Profit_Constraint"

# Solve the problem
problem.solve()

# Output results
batches_produced = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

print(f"Batches produced: {batches_produced}")
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')