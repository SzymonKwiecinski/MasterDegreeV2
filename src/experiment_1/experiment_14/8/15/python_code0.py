import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])
M = len(data['machine_costs'])
TimeRequired = data['time_required']
MachineCosts = data['machine_costs']
Availability = data['availability']
Prices = data['prices']
MinBatches = data['min_batches']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(Prices[p] * x[p] for p in range(P))
costs = pulp.lpSum(MachineCosts[m] * pulp.lpSum(TimeRequired[m][p] * x[p] for p in range(P)) for m in range(M))
problem += profit - costs

# Constraints
# Non-negativity and Minimum production requirement constraints
for p in range(P):
    problem += x[p] >= MinBatches[p], f"MinBatches_Constraint_{p}"

# Machine time availability constraints
for m in range(M):
    problem += pulp.lpSum(TimeRequired[m][p] * x[p] for p in range(P)) <= Availability[m], f"Availability_Constraint_{m}"

# Solve the problem
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')