import pulp

# Data from the provided JSON format
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
TimeRequired = data['time_required']  # Time required to produce one batch
MachineCosts = data['machine_costs']  # Costs associated with using machines
Availability = data['availability']  # Availability of machines
Prices = data['prices']  # Selling prices of parts
MinBatches = data['min_batches']  # Minimum number of batches to produce

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)  # Number of batches for each part

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum([Prices[p] * x[p] for p in range(P)]) - \
         pulp.lpSum([MachineCosts[m] * pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) for m in range(M)])

problem += profit

# Constraints
# Machine time availability constraints
for m in range(M):
    problem += pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) <= Availability[m]

# Minimum production requirement constraints
for p in range(P):
    problem += x[p] >= MinBatches[p]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')