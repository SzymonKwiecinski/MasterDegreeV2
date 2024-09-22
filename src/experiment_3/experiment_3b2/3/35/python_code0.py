import pulp
import json

# Data in JSON format
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

# Extracting data
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create a Linear Programming problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(N+1), lowBound=0, upBound=capacity)

# Objective Function
profit = pulp.lpSum(price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N))
problem += profit

# Constraints
problem += (stock[0] == 0)  # Initial Condition

for n in range(1, N + 1):
    problem += (stock[n] == stock[n-1] + buyquantity[n-1] - sellquantity[n-1])  # Stock Balance
    problem += (stock[n] <= capacity)  # Capacity Constraint

problem += (stock[N] == 0)  # End Condition

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')