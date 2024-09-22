import json
import pulp

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extract parameters
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Number of periods
N = len(prices)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum((sellquantity[n] * prices[n] - buyquantity[n] * costs[n] - stock[n] * holding_cost) for n in range(N))
problem += profit

# Constraints
problem += (stock[0] == 0)  # Initial stock is zero
for n in range(N):
    if n > 0:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n])  # Stock balance constraint
    
    problem += (stock[n] <= capacity)  # Capacity constraint

# Ensuring all stock is sold by the end period
problem += (stock[N-1] == 0)

# Solve the problem
problem.solve()

# Prepare output
output = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result
print(json.dumps(output))