import pulp
import json

data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}

# Extracting the data
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Creating the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: amount of each good to produce
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function: Maximize total revenue
problem += pulp.lpSum(prices[j] * amount[j] for j in range(M))

# Constraints: raw material usage must not exceed available amounts
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i]

# Solve the problem
problem.solve()

# Extract the amount produced for each good
result = [amount[j].varValue for j in range(M)]

# Output the result
output = {"amount": result}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')