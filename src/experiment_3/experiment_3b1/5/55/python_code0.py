import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000,
}

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create a linear programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision variables: batches of each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective function: Maximize total profit
total_time_1 = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))  # total_time_1 for machine 1
labor_cost = pulp.LpVariable("labor_cost")

# Labor cost equation
problem += (labor_cost == (data['standard_cost'] * total_time_1) if total_time_1 <= data['overtime_hour'] 
            else (data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (total_time_1 - data['overtime_hour'])))

# Objective function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - pulp.lpSum(data['machine_costs'][m] * (data['time_required'][m][p] * batches[p] / 100) for m in range(M) for p in range(P)) - labor_cost
problem += profit

# Constraints

# Machine time availability
for m in range(M):
    problem += (pulp.lpSum(data['time_required[m][p]'] * batches[p] / 100 for p in range(P)) <= data['availability'][m])

# Minimum batches required for each part
for p in range(P):
    problem += (batches[p] >= data['min_batches'][p])

# Minimum profit requirement
problem += (profit >= data['min_profit'])

# Solve the problem
problem.solve()

# Output results
batches_produced = {f'batches_{p}': batches[p].varValue for p in range(P)}
total_profit = pulp.value(problem.objective)

for part, produced in batches_produced.items():
    print(f'{part}: {produced}')

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')