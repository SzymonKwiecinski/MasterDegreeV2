import pulp

# Parse the input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data["capacity"]
holding_cost = data["holding_cost"]
prices = data["price"]
costs = data["cost"]

# Number of periods
N = len(prices)

# Create a linear programming problem to maximize profit
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Variables
buy_quantity = [pulp.LpVariable(f"buy_quantity_{n}", lowBound=0, cat='Continuous') for n in range(N)]
sell_quantity = [pulp.LpVariable(f"sell_quantity_{n}", lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0, cat='Continuous') for n in range(N)]

# Objective
# Maximize profit: total revenue - total purchase cost - holding cost
revenue = pulp.lpSum(prices[n] * sell_quantity[n] for n in range(N))
purchase_cost = pulp.lpSum(costs[n] * buy_quantity[n] for n in range(N))
holding_cost_total = pulp.lpSum(holding_cost * stock[n] for n in range(N))

profit = revenue - purchase_cost - holding_cost_total
problem += profit

# Constraints
# Initial stock is 0
problem += stock[0] == buy_quantity[0] - sell_quantity[0], "Initial_Stock"

# Stock balance
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buy_quantity[n] - sell_quantity[n], f"Stock_Balance_{n}"

# Final stock should be 0
problem += stock[N-1] == 0, "Final_Stock"

# Limit stock by warehouse capacity
for n in range(N):
    problem += stock[n] <= capacity, f"Capacity_Constraint_{n}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buyquantity": [pulp.value(buy_quantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sell_quantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')