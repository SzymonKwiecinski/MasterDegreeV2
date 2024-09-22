import pulp

# Data input
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Problem definition
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

# Decision variables
buyquantity = [pulp.LpVariable(f"buy_{n}", lowBound=0, cat='Continuous') for n in range(N)]
sellquantity = [pulp.LpVariable(f"sell_{n}", lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0, cat='Continuous') for n in range(N)]

# Objective function: Maximize profit
profit = pulp.lpSum([sellquantity[n] * price[n] - buyquantity[n] * cost[n] - stock[n] * holding_cost for n in range(N)])
problem += profit

# Constraints
problem += stock[0] == buyquantity[0] - sellquantity[0], "Initial_Stock"
problem += stock[N-1] == 0, "Final_Stock_Empty"

for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}"
    problem += stock[n] <= capacity, f"Capacity_Limit_{n}"

# Solve the problem
problem.solve()

# Gather the results
buy_results = [pulp.value(buyquantity[n]) for n in range(N)]
sell_results = [pulp.value(sellquantity[n]) for n in range(N)]
stock_results = [pulp.value(stock[n]) for n in range(N)]

results = {
    "buyquantity": buy_results,
    "sellquantity": sell_results,
    "stock": stock_results
}

# Output results
print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')