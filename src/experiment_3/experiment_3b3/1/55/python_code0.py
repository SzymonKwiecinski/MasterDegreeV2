import pulp

# Data input
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

# Define the Linear Programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Variables: number of batches for each part
b = [pulp.LpVariable(f'b_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Time used on the labor machine (Machine 1)
time_used = pulp.lpSum([data['time_required'][0][p] * b[p] for p in range(P)])

# Total machine cost for each machine
total_time = [pulp.lpSum([data['time_required'][m][p] * b[p] for p in range(P)]) for m in range(M)]

# Labor cost calculation
labor_cost = pulp.LpVariable("Labor_Cost", lowBound=0, cat='Continuous')
problem += labor_cost >= data['standard_cost'] * time_used
problem += labor_cost >= (data['standard_cost'] * data['overtime_hour'] + 
                          data['overtime_cost'] * (time_used - data['overtime_hour']))

# Objective function
total_income = pulp.lpSum([data['prices'][p] * b[p] for p in range(P)])
total_machine_costs = pulp.lpSum([data['machine_costs'][m] * total_time[m] for m in range(M)])
problem += total_income - total_machine_costs - labor_cost, "Total_Profit"

# Constraints

# Machine time availability constraints
for m in range(M):
    problem += total_time[m] <= data['availability'][m], f"Machine_{m}_Availability"

# Minimum batches required for each part
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Min_Batches_{p}"

# Minimum profit requirement
problem += (total_income - total_machine_costs - labor_cost) >= data['min_profit'], "Min_Profit"

# Solve the problem
problem.solve()

# Output results
batches_produced = [pulp.value(b[p]) for p in range(P)]
print("Batches Produced:", batches_produced)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')