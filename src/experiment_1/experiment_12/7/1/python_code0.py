import pulp

# Data
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [
        [3, 2, 0, 0, 0],
        [0, 5, 2, 1, 0],
        [1, 0, 0, 5, 3],
        [0, 3, 1, 1, 5]
    ],
    'Prices': [7, 10, 5, 9]
}

# Number of goods and raw materials
M = data['M']
N = data['N']
Available = data['Available']
Requirements = data['Requirements']
Prices = data['Prices']

# Define the problem
problem = pulp.LpProblem("Maximize_Total_Revenue", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(M)]

# Objective Function
problem += pulp.lpSum([Prices[i] * x[i] for i in range(M)]), "Total_Revenue"

# Constraints
# Raw material availability constraints
for j in range(N):
    problem += pulp.lpSum([Requirements[i][j] * x[i] for i in range(M)]) <= Available[j], f"Material_{j+1}_Constraint"

# Solve the problem
problem.solve()

# Print the results
print(f'Status: {pulp.LpStatus[problem.status]}')
for i in range(M):
    print(f'x_{i}: {x[i].varValue}')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')