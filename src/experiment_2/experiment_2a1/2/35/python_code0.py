import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Parameters
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective Function: Maximize profit
profit = pulp.lpSum([sellquantity[n] * price[n] - buyquantity[n] * cost[n] - holding_cost * stock[n] for n in range(N)])
problem += profit

# Constraints
# Capacity constraint and stock balance
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n], f"StockBalance_{n}"
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"StockBalance_{n}"
    problem += stock[n] <= capacity, f"CapacityConstraint_{n}"

# Ending stock must be 0
problem += stock[N-1] == 0, "EndingStockConstraint"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buyquantity": [buyquantity[n].varValue for n in range(N)],
    "sellquantity": [sellquantity[n].varValue for n in range(N)],
    "stock": [stock[n].varValue for n in range(N)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')