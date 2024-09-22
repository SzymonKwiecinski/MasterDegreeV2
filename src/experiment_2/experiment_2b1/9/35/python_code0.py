import pulp
import json

data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extract data from the input
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision variables
buyquantities = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0, upBound=capacity) for n in range(N)]
sellquantities = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0, upBound=capacity) for n in range(N)]
stocks = [pulp.LpVariable(f'stock_{n}', lowBound=0, upBound=capacity) for n in range(N)]

# Objective function
profit = pulp.lpSum([(prices[n] * sellquantities[n]) - (costs[n] * buyquantities[n]) - (holding_cost * stocks[n]) for n in range(N)])
problem += profit

# Constraints
for n in range(N):
    if n == 0:
        # Initial stock is zero
        problem += stocks[n] == buyquantities[n] - sellquantities[n]
    else:
        # Stock balance
        problem += stocks[n] == stocks[n-1] + buyquantities[n] - sellquantities[n]

# Capacity constraint
for n in range(N):
    problem += stocks[n] <= capacity

# Ensure warehouse is empty at the end
problem += stocks[N-1] == 0

# Solve the problem
problem.solve()

# Prepare output
output = {
    "buyquantity": [pulp.value(buyquantities[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantities[n]) for n in range(N)],
    "stock": [pulp.value(stocks[n]) for n in range(N)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result
print(json.dumps(output))