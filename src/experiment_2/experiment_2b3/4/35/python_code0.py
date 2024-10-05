import pulp

# Define data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Operation_Optimization", pulp.LpMaximize)

# Define decision variables
buy = [pulp.LpVariable(f'buy_{n}', lowBound=0, cat='Continuous') for n in range(N)]
sell = [pulp.LpVariable(f'sell_{n}', lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, cat='Continuous') for n in range(N)]

# Objective function: Maximize profit
profit = pulp.lpSum([prices[n] * sell[n] - costs[n] * buy[n] - holding_cost * stock[n] for n in range(N)])
problem += profit

# Constraints
for n in range(N):
    # Capacity constraint
    problem += stock[n] <= capacity, f"Capacity_Constraint_{n}"

    # Stock balance for each period
    if n == 0:
        # Initial period, initial stock is 0
        problem += stock[n] == buy[n] - sell[n], f"Stock_Balance_Constraint_{n}"
    else:
        # Subsequent periods
        problem += stock[n] == stock[n-1] + buy[n] - sell[n], f"Stock_Balance_Constraint_{n}"

# Final stock must be zero
problem += stock[N-1] == 0, "Final_Stock_Constraint"

# Solve the problem
problem.solve()

# Create output
output = {
    "buyquantity": [pulp.value(buy[n]) for n in range(N)],
    "sellquantity": [pulp.value(sell[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')