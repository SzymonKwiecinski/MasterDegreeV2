import pulp
import json

data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 
        'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], 
                         [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 
        'Prices': [7, 10, 5, 9]}

# Extracting data
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: amount produced for each good
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function: Maximize total revenue
problem += pulp.lpSum(prices[j] * amount[j] for j in range(M)), "Total_Revenue"

# Constraints: Raw material availability
for i in range(N):
    problem += (pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i]), f"Material_Constraint_{i}"

# Solve the problem
problem.solve()

# Prepare the result
result = {
    "amount": [amount[j].varValue for j in range(M)]
}

print(json.dumps(result))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')