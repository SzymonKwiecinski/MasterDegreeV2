import pulp

# Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Number of spare parts and machines
K = len(data['profit'])  # Number of different spare parts
S = len(data['capacity'])  # Number of machines

# Create a linear programming problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
# Machine capacity constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the results
for k in range(K):
    print(f'Quantity of spare part {k + 1} to produce: {pulp.value(x[k])}')
    
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')