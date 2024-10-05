import pulp

# Define the data
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

# Extracting data from the json
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Initialize the Linear Program
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective Function
problem += pulp.lpSum(prices[j] * amount[j] for j in range(M))

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i]

# Solve the problem
problem.solve()

# Extract Solution
output = {
    "amount": [pulp.value(amount[j]) for j in range(M)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')