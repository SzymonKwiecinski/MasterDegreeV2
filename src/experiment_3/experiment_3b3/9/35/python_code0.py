import pulp

# Data input
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extracting data
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Problem definition
problem = pulp.LpProblem("Warehouse_Operations_Optimization", pulp.LpMaximize)

# Variables
buyquantity = [pulp.LpVariable(f"buyquantity_{n}", lowBound=0) for n in range(1, N + 1)]
sellquantity = [pulp.LpVariable(f"sellquantity_{n}", lowBound=0) for n in range(1, N + 1)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0) for n in range(N + 1)]

# Objective function
problem += pulp.lpSum(
    price[n - 1] * sellquantity[n - 1] - cost[n - 1] * buyquantity[n - 1] - holding_cost * stock[n]
    for n in range(1, N + 1)
), "Total_Profit"

# Initial stock condition
problem += stock[0] == 0, "Initial_Stock"

# Constraints
for n in range(1, N + 1):
    # Stock balance constraint
    problem += stock[n] == stock[n - 1] + buyquantity[n - 1] - sellquantity[n - 1], f"Stock_Balance_{n}"
    # Capacity constraint
    problem += stock[n] <= capacity, f"Capacity_Constraint_{n}"

# Final stock condition
problem += stock[N] == 0, "Final_Stock"

# Solving the problem
problem.solve()

# Output the results
buy_quantity = [pulp.value(buyquantity[n - 1]) for n in range(1, N + 1)]
sell_quantity = [pulp.value(sellquantity[n - 1]) for n in range(1, N + 1)]
stock_levels = [pulp.value(stock[n]) for n in range(1, N + 1)]

result = {
    "buyquantity": buy_quantity,
    "sellquantity": sell_quantity,
    "stock": stock_levels
}

print("Optimization Result:", result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')