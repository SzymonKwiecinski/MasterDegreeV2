import pulp

# Data input
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Initialize the problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision variables
buyquantity = [pulp.LpVariable(f"buyquantity_{n}", lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f"sellquantity_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0) for n in range(N)]

# Objective function: maximize profit
profit = pulp.lpSum([sellquantity[n] * price[n] - buyquantity[n] * cost[n] - stock[n] * holding_cost for n in range(N)])
problem += profit

# Constraints
for n in range(N):
    if n == 0:
        problem += buyquantity[n] - sellquantity[n] == stock[n], f"StockBalance_{n}"
    else:
        problem += stock[n-1] + buyquantity[n] - sellquantity[n] == stock[n], f"StockBalance_{n}"

    problem += stock[n] <= capacity, f"Capacity_{n}"

# Constraint for final stock to be zero
problem += stock[N-1] == 0, "FinalStockZero"

# Solve the problem
problem.solve()

# Create the output dictionary
output = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

# Display results
print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')