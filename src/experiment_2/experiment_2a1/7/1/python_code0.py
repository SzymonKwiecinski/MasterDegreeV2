import pulp
import json

# Input data
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 
        'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 
        'Prices': [7, 10, 5, 9]}
        
M = data['M']  # Number of goods
N = data['N']  # Number of raw materials
available = data['Available']  # Available amount of raw materials
requirements = data['Requirements']  # Requirements for each good
prices = data['Prices']  # Prices for each good

# Create a LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: amount of each good produced
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function: Maximize total revenue
problem += pulp.lpSum(prices[j] * amount[j] for j in range(M)), "Total_Revenue"

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i], f"Resource_Constraint_{i}"

# Solve the problem
problem.solve()

# Collect the results
amounts_produced = [amount[j].varValue for j in range(M)]

# Output the result
result = {"amount": amounts_produced}
print(result)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')