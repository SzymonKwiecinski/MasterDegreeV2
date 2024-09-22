import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Parameters
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

# Decision variables
buy_quantities = [pulp.LpVariable(f'buy_{n}', lowBound=0) for n in range(N)]
sell_quantities = [pulp.LpVariable(f'sell_{n}', lowBound=0) for n in range(N)]
stocks = [pulp.LpVariable(f'stock_{n}', lowBound=0) for n in range(N)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[n] - costs[n]) * sell_quantities[n] - holding_cost * stocks[n] for n in range(N)])
problem += profit

# Constraints
# Capacity constraint for each period
for n in range(N):
    if n == 0:
        problem += buy_quantities[n] - sell_quantities[n] <= capacity
    else:
        problem += stocks[n-1] + buy_quantities[n] - sell_quantities[n] <= capacity
    # Stock balance
    problem += stocks[n] == (stocks[n-1] + buy_quantities[n] - sell_quantities[n]) if n > 0 else buy_quantities[n] - sell_quantities[n]

# Ending condition: stock must be empty at the end
problem += stocks[-1] == 0

# Solve the problem
problem.solve()

# Collect results
buy_quantities_result = [pulp.value(buy_quantities[n]) for n in range(N)]
sell_quantities_result = [pulp.value(sell_quantities[n]) for n in range(N)]
stocks_result = [pulp.value(stocks[n]) for n in range(N)]

# Output results
output = {
    "buyquantity": buy_quantities_result,
    "sellquantity": sell_quantities_result,
    "stock": stocks_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')