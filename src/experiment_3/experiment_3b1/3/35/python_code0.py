import pulp

# Given data
data = {
    'capacity': 10, 
    'holding_cost': 2, 
    'price': [1, 2, 100], 
    'cost': [100, 1, 100]
}

# Parameters
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Create the problem
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", range(N), lowBound=0, upBound=capacity, cat='Continuous')

# Objective function
profit = pulp.lpSum(sellquantity[n] * prices[n] - buyquantity[n] * costs[n] - (stock[n-1] if n > 0 else 0) * holding_cost for n in range(N))
problem += profit

# Constraints for stock balance and capacity
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n]
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]
    
    problem += stock[n] <= capacity

# Final stock condition
problem += stock[N-1] == 0

# Solve the problem
problem.solve()

# Print the results
buyquantity_values = [pulp.value(buyquantity[n]) for n in range(N)]
sellquantity_values = [pulp.value(sellquantity[n]) for n in range(N)]
stock_values = [pulp.value(stock[n]) for n in range(N)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print('Buy quantities:', buyquantity_values)
print('Sell quantities:', sellquantity_values)
print('Stock levels:', stock_values)