import pulp

# Data from the given JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines
TimeRequired = data['time_required']
MachineCosts = data['machine_costs']
Availability = data['availability']
Prices = data['prices']
MinBatches = data['min_batches']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum(Prices[p] * x[p] for p in range(P)) - \
         pulp.lpSum(MachineCosts[m] * pulp.lpSum(TimeRequired[m][p] * x[p] for p in range(P)) for m in range(M))
problem += profit

# Constraints
# Machine time availability constraints
for m in range(M):
    problem += pulp.lpSum(TimeRequired[m][p] * x[p] for p in range(P)) <= Availability[m], f"Machine_Availability_{m}"

# Minimum production requirement
for p in range(P):
    problem += x[p] >= MinBatches[p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Print the results
for p in range(P):
    print(f'Batches of part {p + 1}: {pulp.value(x[p])}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')