import pulp

# Data
M = 4  # number of different goods
N = 5  # number of different raw materials
available = [10, 20, 15, 35, 25]
requirements = [
    [3, 2, 0, 0],
    [0, 5, 2, 1],
    [1, 0, 0, 5],
    [0, 3, 1, 1],
    [5, 0, 3, 0]  # Added a valid row for the 5th raw material
]
prices = [7, 10, 5, 9]

# Problem
problem = pulp.LpProblem('Maximize_Revenue', pulp.LpMaximize)

# Variables
amount = [pulp.LpVariable(f'amount_{j+1}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective
problem += pulp.lpSum(prices[j] * amount[j] for j in range(M))

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * amount[j] for j in range(M)) <= available[i]

# Solve
problem.solve()

# Output Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')