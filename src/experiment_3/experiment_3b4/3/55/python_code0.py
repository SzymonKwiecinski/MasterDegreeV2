import pulp

# Data provided
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

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(4), lowBound=0, cat='Continuous')
hours_1 = pulp.LpVariable("hours_1", lowBound=0, cat='Continuous')

# Objective function
profit = (
    pulp.lpSum(
        data['prices'][p] * batches[p] for p in range(4)
    ) 
    - pulp.lpSum(
        data['machine_costs'][m] * data['time_required'][m][p] * batches[p] 
        for m in range(1, 3) for p in range(4)
    ) 
    - (
        data['standard_cost'] * pulp.lpSum(min(hours_1, data['overtime_hour'])) +
        data['overtime_cost'] * pulp.lpSum(max(0, hours_1 - data['overtime_hour']))
    )
)
problem += profit

# Constraints
for m in range(1, 3):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(4)) <= data['availability'][m]

problem += pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(4)) == hours_1

for p in range(4):
    problem += batches[p] >= data['min_batches'][p]

problem += profit >= data['min_profit']

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')