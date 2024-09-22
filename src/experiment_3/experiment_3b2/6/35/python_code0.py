import pulp
import json

# Data
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(1, N+1), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(1, N+1), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(0, N+1), lowBound=0)

# Objective function
problem += pulp.lpSum(price[n-1] * sellquantity[n] - cost[n-1] * buyquantity[n] - holding_cost * stock[n] for n in range(1, N+1))

# Constraints
# Capacity constraint
for n in range(1, N+1):
    problem += stock[n] <= capacity

# Balance constraints
for n in range(1, N+1):
    if n == 1:
        problem += stock[n] == buyquantity[n] - sellquantity[n]
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

# Initial and Final stock constraints
problem += stock[0] == 0  # Initial stock
problem += stock[N] == 0   # Final stock

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')