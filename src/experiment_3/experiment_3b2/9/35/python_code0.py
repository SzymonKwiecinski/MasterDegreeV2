import pulp
import json

# Data from JSON
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
N = len(data['price'])
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)
y = pulp.LpVariable.dicts("y", range(N), lowBound=0)
s = pulp.LpVariable.dicts("s", range(N + 1), lowBound=0)

# Objective function
profit = pulp.lpSum(data['price'][n] * y[n] - data['cost'][n] * x[n] for n in range(N))
holding_cost = pulp.lpSum(data['holding_cost'] * s[n] for n in range(N))
problem += profit - holding_cost

# Constraints
for n in range(N):
    problem += s[n] <= data['capacity'], f"Capacity_Constraint_{n}"
    if n == 0:
        problem += s[0] == 0, "Initial_Stock_0"
    else:
        problem += s[n] == s[n - 1] + x[n - 1] - y[n - 1], f"Stock_Balance_{n}"

problem += s[N] == 0, "Final_Stock_Condition"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')