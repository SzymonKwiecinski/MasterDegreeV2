import pulp
import json

# Input Data
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 
        'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], 
                        [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 
        'Prices': [7, 10, 5, 9]}

# Problem Setup
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective Function
problem += pulp.lpSum([prices[j] * amount[j] for j in range(M)])

# Constraints
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i]

# Solve the problem
problem.solve()

# Output result
result = { "amount": [pulp.value(amount[j]) for j in range(M)] }
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')