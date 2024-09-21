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

# Unpack data
M = data['M']
N = data['N']
Available = data['Available']
Requirements = data['Requirements']
Prices = data['Prices']

# Initialize the linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(M)]

# Objective function
problem += pulp.lpSum([Prices[i] * x[i] for i in range(M)])

# Constraints for raw material usage
for j in range(N):
    problem += (pulp.lpSum([Requirements[i][j] * x[i] for i in range(M)]) <= Available[j])

# Solve the linear programming problem
problem.solve()

# Output the results
for i in range(M):
    print(f'Quantity of good {i+1} produced: {pulp.value(x[i])}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')