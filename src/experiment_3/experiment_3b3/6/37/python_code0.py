import pulp

# Data from the JSON format
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}

# Extracting data
time = data['time']
profit = data['profit']
capacity = data['capacity']
K = len(profit)
S = len(capacity)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
q = [pulp.LpVariable(f'q_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * q[k] for k in range(K)), "Total Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * q[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the quantities of each spare part to be produced
quantity = [pulp.value(q[k]) for k in range(K)]
print(f'Quantity of each spare part to be produced: {quantity}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')