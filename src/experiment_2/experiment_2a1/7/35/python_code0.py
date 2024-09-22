import pulp
import json

# Given data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extracting parameters
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective Function: Maximize profit
profit = pulp.lpSum((price[n] - cost[n]) * sellquantity[n] - holding_cost * stock[n] for n in range(N))
problem += profit

# Constraints
# Capacity constraint and final stock must be zero
problem += pulp.lpSum(buyquantity[n] for n in range(N)) <= capacity, "CapacityConstraint"
problem += stock[0] == buyquantity[0] - sellquantity[0], "InitialStock"
for n in range(1, N):
    problem += stock[n] == stock[n - 1] + buyquantity[n] - sellquantity[n], f"StockBalance_{n}"
problem += stock[N - 1] == 0, "FinalStock"

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