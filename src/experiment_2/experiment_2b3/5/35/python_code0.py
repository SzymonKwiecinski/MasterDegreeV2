import pulp

data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Unpacking data
capacity = data["capacity"]
holding_cost = data["holding_cost"]
prices = data["price"]
costs = data["cost"]
N = len(prices)

# Define the Linear Programming problem
problem = pulp.LpProblem("Warehouse_Operation_Max_Profit", pulp.LpMaximize)

# Decision variables
buy_quantity = [pulp.LpVariable(f"buy_quantity_{n}", lowBound=0, cat='Continuous') for n in range(N)]
sell_quantity = [pulp.LpVariable(f"sell_quantity_{n}", lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0, upBound=capacity, cat='Continuous') for n in range(N)]

# Objective function: Maximize Profit
profit_terms = [prices[n] * sell_quantity[n] - costs[n] * buy_quantity[n] - holding_cost * stock[n] for n in range(N)]
problem += pulp.lpSum(profit_terms), "Total Profit"

# Constraints
# Initial and final stock conditions
problem += stock[0] == buy_quantity[0] - sell_quantity[0], "Initial Stock Balance"
problem += stock[N-1] == 0, "Final Stock Zero"

# Stock balance for each period
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buy_quantity[n] - sell_quantity[n], f"Stock Balance Period {n}"

# Solve the problem
problem.solve()

# Results
output = {
    "buyquantity": [pulp.value(buy_quantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sell_quantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')