import pulp

# Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Parameters
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of spare parts (K) and machines (S)
K = len(profit)
S = len(capacity)

# Define Problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K))

# Constraints
# Capacity constraints for each machine
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_Machine_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')