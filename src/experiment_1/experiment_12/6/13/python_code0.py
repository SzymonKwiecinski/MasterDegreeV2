import pulp

# Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Constants from data
K = len(data['profit'])  # Number of spare parts
S = len(data['capacity'])  # Number of machines

# Parameters from data
Time = data['time']
Profit = data['profit']
Capacity = data['capacity']

# Define the problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(K)]), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum([Time[k][s] * x[k] for k in range(K)]) <= Capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')