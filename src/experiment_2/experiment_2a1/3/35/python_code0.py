import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Initialize the problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum([sellquantity[n] * price[n] - buyquantity[n] * cost[n] - holding_cost * stock[n] for n in range(N)])
problem += profit

# Constraints
problem += (pulp.lpSum(buyquantity[n] for n in range(N)) <= capacity, "Capacity Constraint")

# Stock balance constraints
for n in range(N):
    if n == 0:
        problem += (stock[n] == buyquantity[n] - sellquantity[n], f"Stock Balance {n}")
    else:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock Balance {n}")

# Final stock must be zero
problem += (stock[N-1] == 0, "Final Stock Constraint")

# Solve the problem
problem.solve()

# Output the results
result = {
    "buyquantity": [buyquantity[n].varValue for n in range(N)],
    "sellquantity": [sellquantity[n].varValue for n in range(N)],
    "stock": [stock[n].varValue for n in range(N)]
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the result
print(json.dumps(result))