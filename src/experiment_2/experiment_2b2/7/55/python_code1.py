import pulp

# Problem data
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

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
P = len(data['prices'])
M = len(data['machine_costs'])
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]
overtime_hours_regular = pulp.LpVariable('overtime_hours_regular', lowBound=0, upBound=data['overtime_hour'], cat='Continuous')
overtime_hours_extra = pulp.LpVariable('overtime_hours_extra', lowBound=0, cat='Continuous')

# Objective function: Maximize Profit
profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)])
machine_costs = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(1, M)])
overtime_cost = data['standard_cost'] * overtime_hours_regular + data['overtime_cost'] * overtime_hours_extra
problem += profit - machine_costs - overtime_cost, "Total_Profit"

# Constraints
for m in range(1, M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Machine_{m}_Availability"

# Special constraints for Machine 1 (outsource cost)
total_overtime_hours = overtime_hours_regular + overtime_hours_extra
problem += pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) == total_overtime_hours, "Outsource_Machine_1"

# Minimal profit constraint
problem += profit - machine_costs - overtime_cost >= data['min_profit'], "Minimum_Profit"

# Solve the problem
problem.solve()

# Prepare results
batches_produced = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(profit - machine_costs - overtime_cost)

output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')