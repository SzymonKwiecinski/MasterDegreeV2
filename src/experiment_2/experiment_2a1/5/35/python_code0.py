import pulp
import json

# Given Data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Initialize the problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum((prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N))
problem += profit

# Constraints
# Capacity constraint for each period
for n in range(N):
    problem += (stock[n] + buyquantity[n] - sellquantity[n] <= capacity, f"Capacity_Constraint_{n}")
    
# Stock balance for each period
for n in range(N):
    if n == 0:
        problem += (stock[n] == buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}")
    else:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}")

# Final stock must be zero
problem += (stock[N-1] == 0, "Final_Stock_Constraint")

# Solve the problem
problem.solve()

# Collecting results
buyquantity_results = [buyquantity[n].varValue for n in range(N)]
sellquantity_results = [sellquantity[n].varValue for n in range(N)]
stock_results = [stock[n].varValue for n in range(N)]

# Output
output = {
    "buyquantity": buyquantity_results,
    "sellquantity": sellquantity_results,
    "stock": stock_results
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')