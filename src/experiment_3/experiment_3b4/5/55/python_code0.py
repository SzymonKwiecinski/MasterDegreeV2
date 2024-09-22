import pulp

# Data from JSON
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

# Indices
P = len(data['prices'])
M = len(data['machine_costs'])

# Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')
overtime_1 = pulp.LpVariable("Overtime_1", lowBound=0, cat='Continuous')

# Objective Function
total_revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
total_cost = (pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(1, M))
             + data['standard_cost'] * pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) 
             + data['overtime_cost'] * overtime_1)
total_profit = total_revenue - total_cost

problem += total_profit, "Total_Profit"

# Constraints

# Machine time constraints (for machines 2 to M)
for m in range(1, M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]), f"Machine_{m}_Constraint"

# Machine 1 time and overtime constraints
problem += (pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) <= data['overtime_hour'] + overtime_1), "Machine_1_Constraint"

# Minimum production requirements
for p in range(P):
    problem += (batches[p] >= data['min_batches'][p]), f"Min_Production_{p}"

# Profit requirement
problem += (total_profit >= data['min_profit']), "Profit_Requirement"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')