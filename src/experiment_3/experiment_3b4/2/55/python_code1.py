import pulp

# Data
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

P = len(data['prices'])
M = len(data['availability'])

# Decision Variables
x = pulp.LpVariable.dicts('x', range(P), lowBound=0, cat='Continuous')

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Calculate labor time for machine 1
h1 = pulp.lpSum([data['time_required'][0][p] * x[p] for p in range(P)])

# Labor Cost on Machine 1
labor_cost_condition = pulp.LpVariable('Labor_Cost_Condition', cat='Binary')
labor_cost_overtime = labor_cost_condition * data['overtime_cost'] * (h1 - data['overtime_hour'])
labor_cost_standard = (1 - labor_cost_condition) * data['standard_cost'] * data['overtime_hour']
labor_cost = data['standard_cost'] * h1 + pulp.lpSum([labor_cost_overtime, labor_cost_standard])

# Objective Function: Maximize Profit
profit = (
    pulp.lpSum([data['prices'][p] * x[p] for p in range(P)]) 
    - pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) for m in range(1, M)])
    - labor_cost
)
problem += profit

# Constraints

# Demand Constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Machine Availability (excluding machine 1)
for m in range(1, M):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) <= data['availability'][m]

# Profit Constraint
problem += profit >= data['min_profit']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')