from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

# Data from JSON
data = {
    "M": 4,
    "N": 5,
    "Available": [10, 20, 15, 35, 25],
    "Requirements": [
        [3, 2, 0, 0, 0],
        [0, 5, 2, 1, 0],
        [1, 0, 0, 5, 3],
        [0, 3, 1, 1, 5]
    ],
    "Prices": [7, 10, 5, 9]
}

# Extract data
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Create the LP problem
problem = LpProblem("Maximize Revenue", LpMaximize)

# Decision variables: amount of each good to produce
amount = [LpVariable(f'amount_{j}', lowBound=0) for j in range(M)]

# Objective function: Maximize revenue
problem += lpSum(prices[j] * amount[j] for j in range(M))

# Constraints: Cannot exceed available materials
for i in range(N):
    problem += lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "amount": [value(amount[j]) for j in range(M)]
}

# Print the result
print(output)

# Print the objective value
print(f'(Objective Value): <OBJ>{value(problem.objective)}</OBJ>')