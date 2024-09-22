import json
import pulp

data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Number of periods
N = len(prices)

# Create the linear programming problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Define decision variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum((prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N))
problem += profit

# Constraints
problem += stock[0] == 0  # Starting stock is zero

for n in range(N):
    problem += stock[n] <= capacity  # Capacity constraint
    problem += stock[n] == (stock[n-1] + buyquantity[n-1] - sellquantity[n-1]) if n > 0 else (buyquantity[n] - sellquantity[n])

problem += stock[N-1] == 0  # Ending stock is zero

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buyquantity": [buyquantity[n].varValue for n in range(N)],
    "sellquantity": [sellquantity[n].varValue for n in range(N)],
    "stock": [stock[n].varValue for n in range(N)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')