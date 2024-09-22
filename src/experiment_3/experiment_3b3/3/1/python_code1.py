import pulp

# Extract data from JSON format
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 
        'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], 
                         [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 
        'Prices': [7, 10, 5, 9]}

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Create variables
x = [pulp.LpVariable(f'x{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function
problem += pulp.lpSum(prices[j] * x[j] for j in range(M)), "Total Revenue"

# Constraints
for i in range(N):
    problem += (pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i]), f"Material_{i}_Constraint"

# Solve the problem
problem.solve()

# Output the amounts of each good to be produced
amounts = {f"x{j}": x[j].varValue for j in range(M)}
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Optimal amounts to produce: {amounts}')