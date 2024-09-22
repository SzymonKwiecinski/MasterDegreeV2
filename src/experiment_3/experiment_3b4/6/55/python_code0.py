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

# Constants
P = len(data['prices'])
M = len(data['availability'])

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{p+1}', lowBound=data['min_batches'][p], cat='Integer') for p in range(P)]

# Objective Function
total_profit = (
    pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) -
    (pulp.lpSum(data['time_required'][0][p] * x[p] for p in range(P)) <= data['overtime_hour']) * data['standard_cost'] * pulp.lpSum(data['time_required'][0][p] * x[p] for p in range(P)) +
    (pulp.lpSum(data['time_required'][0][p] * x[p] for p in range(P)) > data['overtime_hour']) * (
        data['standard_cost'] * data['overtime_hour'] +
        data['overtime_cost'] * (pulp.lpSum(data['time_required'][0][p] * x[p] for p in range(P)) - data['overtime_hour']))
)

# Constraints
# Machine Availability (except the first machine)
for m in range(1, M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Profit Constraint
problem += total_profit >= data['min_profit']

# Set the objective
problem += total_profit

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')