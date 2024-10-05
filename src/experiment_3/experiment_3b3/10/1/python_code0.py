import pulp

# Data
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective Function
problem += pulp.lpSum(prices[j] * x[j] for j in range(M)), "Total Revenue"

# Constraints
for i in range(N):
    problem += (pulp.lpSum(requirements[j][i] * x[j] for j in range(M)) <= available[i]), f"Raw Material Constraint {i+1}"

# Solve
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')