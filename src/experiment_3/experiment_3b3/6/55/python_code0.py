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

P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Integer') for p in range(P)]

# Objective function components
total_revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
total_cost = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))

# Total profit
profit = total_revenue - total_cost

# Set the objective
problem += profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m])

# Minimum profit constraint
problem += profit >= data['min_profit']

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')