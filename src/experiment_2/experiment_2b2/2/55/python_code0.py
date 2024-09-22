import pulp

# Input Data
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

# Problem Information
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

M = len(time_required)  # Number of machines
P = len(prices)         # Number of parts

# Initialize the LP Problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision Variables: Number of batches for each part
batches = [pulp.LpVariable(f'batch_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Auxiliary Variables for Machine 1 (for labor cost)
time_on_machine_1 = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
regular_hours_1 = pulp.LpVariable("regular_hours_1", lowBound=0, cat='Continuous')
overtime_hours_1 = pulp.LpVariable("overtime_hours_1", lowBound=0, cat='Continuous')

# Constraints for regular and overtime hours on Machine 1
problem += regular_hours_1 + overtime_hours_1 == time_on_machine_1, "Time_Machine_1"
problem += regular_hours_1 <= overtime_hour, "Regular_Hours_Constraint"

# Constraints for machine availability (except machine 1)
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Machine_{m}"

# Objective Function: Maximize Total Profit
profit = (pulp.lpSum(prices[p] * batches[p] for p in range(P))
          - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(1, M))
          - standard_cost * regular_hours_1
          - overtime_cost * overtime_hours_1)

problem += profit, "Total_Profit"

# Constraint: Desired minimum profit
problem += profit >= min_profit, "Min_Profit"

# Solve the problem
problem.solve()

# Output Results
batches_produced = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(profit)

output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')