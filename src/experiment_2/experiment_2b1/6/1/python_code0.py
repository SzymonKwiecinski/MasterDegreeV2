import pulp
import json

# Input data
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

M = data['M']  # Number of goods
N = data['N']  # Number of raw materials
available = data['Available']  # Available quantities of raw materials
requirements = data['Requirements']  # Requirements of raw materials for each good
prices = data['Prices']  # Prices for each good

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Create decision variables for the amount of each good produced
amounts = [pulp.LpVariable(f"amount_{j}", lowBound=0) for j in range(M)]

# Objective function: maximize total revenue
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M)), "Total_Revenue"

# Constraints: raw material availability
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i], f"Material_Constraint_{i}"

# Solve the problem
problem.solve()

# Prepare the result
result = {
    "amount": [amounts[j].varValue for j in range(M)]
}

# Output the amount produced
print(json.dumps(result))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')