import pulp

# Data from the JSON
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

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'b_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
machine_costs = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))

machine_1_hours = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))
overtime_hours = pulp.LpVariable("overtime_hours", lowBound=0, cat='Continuous')
labor_cost_machine_1 = pulp.LpVariable("labor_cost_machine_1", lowBound=0, cat='Continuous')

# Constraints for Labor Cost on Machine 1
problem += labor_cost_machine_1 == data['standard_cost'] * machine_1_hours + (data['overtime_cost'] - data['standard_cost']) * overtime_hours

# Overtime hours calculation
problem += overtime_hours == machine_1_hours - data['overtime_hour']
problem += overtime_hours >= 0

# Total Profit including labor costs
total_profit = profit - machine_costs - labor_cost_machine_1

# Set the objective function
problem += total_profit

# Constraints

# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Minimum Batch Production Constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Minimum Profit Constraint
problem += total_profit >= data['min_profit']

# Solve the problem
problem.solve()

# Outputs the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the batches for each part
batches_produced = [pulp.value(batches[p]) for p in range(P)]
print("Batches produced:", batches_produced)