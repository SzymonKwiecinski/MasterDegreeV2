import pulp
import json

# Given data in JSON format
data_json = '{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}'
data = json.loads(data_json)

# Problem setup
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantities = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(N)]
sellquantities = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(N)]
stocks = [pulp.LpVariable(f'stock_{n}', lowBound=0, upBound=capacity) for n in range(N)]

# Objective function
profit_expr = pulp.lpSum(prices[n] * sellquantities[n] - costs[n] * buyquantities[n] for n in range(N)) - \
              pulp.lpSum(holding_cost * stocks[n] for n in range(N))
problem += profit_expr

# Constraints
# Initial stock condition
problem += (stocks[0] == 0)

# Stock balance equation and warehouse capacity constraints
for n in range(1, N):
    problem += (stocks[n] == stocks[n - 1] + buyquantities[n] - sellquantities[n])

# Final stock condition
problem += (stocks[N-1] == 0)

# Non-negativity and stock capacity constraints
for n in range(N):
    problem += (stocks[n] >= 0)
    problem += (stocks[n] <= capacity)

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')