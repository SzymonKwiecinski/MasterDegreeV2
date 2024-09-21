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

# Parameters
M = data['M']
N = data['N']
Available = data['Available']
Requirements = data['Requirements']
Prices = data['Prices']

# Problem
problem = pulp.LpProblem("Maximize_Total_Revenue", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(M)]

# Objective Function
problem += pulp.lpSum(Prices[i] * x[i] for i in range(M)), "Total_Revenue"

# Constraints
for j in range(N):
    problem += pulp.lpSum(Requirements[i][j] * x[i] for i in range(M)) <= Available[j], f"Material_{j}_Constraint"

# Solve
problem.solve()

# Results
print(f'Status: {pulp.LpStatus[problem.status]}')
for i in range(M):
    print(f'Quantity of Good {i+1}: {x[i].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')