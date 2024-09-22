import pulp

# Define the data
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
M = len(data['availability'])

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
b = [pulp.LpVariable(f'b_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective function
revenue = pulp.lpSum(data['prices'][p] * b[p] for p in range(P))

# Machine costs
machine_costs = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) for m in range(M))

# Labor Cost for machine 1
labor_hours_machine1 = pulp.lpSum(data['time_required'][0][p] * b[p] for p in range(P))
labor_cost = pulp.LpVariable('labor_cost', lowBound=0, cat='Continuous')

problem += labor_cost == pulp.lpSum([data['standard_cost'] * labor_hours_machine1, 
                                     (data['overtime_cost'] - data['standard_cost']) * pulp.lpSum(labor_hours_machine1 - data['overtime_hour'])])

# Objective function
total_profit = revenue - machine_costs - labor_cost
problem += total_profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) <= data['availability'][m]

# Minimum batches requirements
for p in range(P):
    problem += b[p] >= data['min_batches'][p]

# Minimum profit requirement
problem += total_profit >= data['min_profit']

# Solve the problem
problem.solve()

# Print the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')