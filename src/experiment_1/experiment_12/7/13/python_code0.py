import pulp

# Parse the data from JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
    'profit': [30, 20, 40, 25, 10], 
    'capacity': [700, 1000]
}

time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of different spare parts (K) and machines (S)
K = len(profit)
S = len(capacity)

# Define the LP problem
problem = pulp.LpProblem("Optimal_Spare_Parts_Production", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_Machine_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Optionally display the solution (quantities of each spare part to produce)
for k in range(K):
    print(f'Spare part {k+1}: Produce {x[k].varValue}')