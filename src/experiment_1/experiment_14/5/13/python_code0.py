import pulp

# Define data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Number of spare parts K and machines S
K = len(data['profit'])
S = len(data['capacity'])

# Extract data
Time = data['time']
Profit = data['profit']
Capacity = data['capacity']

# Define the Linear Programming Problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function: Maximize total profit
problem += pulp.lpSum(Profit[k] * x[k] for k in range(K)), "Total Profit"

# Constraints
# Machine capacity constraints
for s in range(S):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(K)) <= Capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')