import pulp

# Data input
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

# Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(data['M'])]

# Objective
problem += pulp.lpSum(data['Prices'][j] * amount[j] for j in range(data['M']))

# Constraints
for i in range(data['N']):
    problem += (
        pulp.lpSum(data['Requirements'][j][i] * amount[j] for j in range(data['M']))
        <= data['Available'][i]
    )

# Solve
problem.solve()

# Output
result = {'amount': [pulp.value(amount[j]) for j in range(data['M'])]}
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')