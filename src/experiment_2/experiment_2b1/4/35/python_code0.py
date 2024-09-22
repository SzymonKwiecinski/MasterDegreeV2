import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extracting the parameters from the input data
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Creating the optimization problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision variables
buyquantities = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0, cat='Continuous')
sellquantities = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0, cat='Continuous')
stocks = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum((prices[n] * sellquantities[n] - costs[n] * buyquantities[n] - holding_cost * stocks[n]) for n in range(N))
problem += profit

# Constraints
# Capacity constraint
problem += (pulp.lpSum(buyquantities[n] for n in range(N)) <= capacity), "Capacity"

# Stock balance for each period
for n in range(N):
    if n == 0:
        problem += (stocks[n] == buyquantities[n] - sellquantities[n]), f"Stock_Balance_{n}"
    else:
        problem += (stocks[n] == stocks[n-1] + buyquantities[n] - sellquantities[n]), f"Stock_Balance_{n}"

# Final stock should be zero
problem += (stocks[N-1] == 0), "Final_Stock_Zero"

# Solving the problem
problem.solve()

# Storing the results
solution = {
    "buyquantity": [buyquantities[n].varValue for n in range(N)],
    "sellquantity": [sellquantities[n].varValue for n in range(N)],
    "stock": [stocks[n].varValue for n in range(N)]
}

# Output the result
print(json.dumps(solution))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')