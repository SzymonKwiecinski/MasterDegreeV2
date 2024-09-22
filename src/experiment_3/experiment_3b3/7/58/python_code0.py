import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'setup_time': [12, 8, 4, 0]
}

P = len(data['prices'])
M = len(data['machine_costs'])

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Initialize the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer_Problem", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
setup_flag = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective Function
total_revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
total_costs = pulp.lpSum(machine_costs[m] * (
    pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
    pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P))
) for m in range(M))
profit = total_revenue - total_costs
problem += profit

# Constraints
# Machine Time Availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + \
               pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')