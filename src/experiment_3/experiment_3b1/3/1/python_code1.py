import pulp
import json

# Data provided in JSON format
data = {
    'M': 4, 
    'N': 5, 
    'Available': [10, 20, 15, 35, 25], 
    'Requirements': [[3, 2, 0, 0], 
                    [0, 5, 2, 1], 
                    [1, 0, 0, 5], 
                    [0, 3, 1, 1]], 
    'Prices': [7, 10, 5, 9]
}

# Extracting data
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

# Objective Function
problem += pulp.lpSum(prices[j] * x[j] for j in range(M)), "Total_Revenue"

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i], f"Material_{i+1}_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the production amounts for each good
for j in range(M):
    print(f'Good {j+1}: {x[j].varValue}')