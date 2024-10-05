import pulp

# Data from JSON
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

# Variables
M = data['M']
N = data['N']
Available = data['Available']
Requirements = data['Requirements']
Prices = data['Prices']

# Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function
problem += pulp.lpSum(Prices[j] * x[j] for j in range(M)), "Total_Revenue"

# Constraints
for i in range(N):
    problem += pulp.lpSum(Requirements[j][i] * x[j] for j in range(M)) <= Available[i], f"Raw_Material_Constraint_{i}"

# Solve the problem
problem.solve()

# Output solution
amount = {f'x_{j}': x[j].varValue for j in range(M)}
print(f'Optimal amounts to produce: {amount}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')