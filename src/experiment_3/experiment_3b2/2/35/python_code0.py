import pulp
import json

# Given data
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(N + 1), lowBound=0)

# Objective function
profit = pulp.lpSum(prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N))
problem += profit

# Constraints
problem += stock[0] == 0  # Initial stock
for n in range(N):
    problem += stock[n] == stock[n - 1] + buyquantity[n] - sellquantity[n]  # Stock balance
    problem += stock[n] <= capacity  # Stock capacity limit
    problem += stock[n] >= 0  # Non-negativity constraint on stock

problem += stock[N] == 0  # End stock should be 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')