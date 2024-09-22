import pulp
import json

# Load data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", range(N), lowBound=0, cat='Continuous')

# Objective Function: Maximize profit
profit = pulp.lpSum((price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N))
problem += profit

# Constraints
# Capacity constraint
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n], f"Stock_Initial_Period"
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock_Period_{n}"
    problem += stock[n] <= capacity, f"Capacity_Constraint_{n}"

# Ending conditions
problem += stock[N-1] == 0, "End_Condition"

# Solve the problem
problem.solve()

# Collect results
buyquantity_result = [pulp.value(buyquantity[n]) for n in range(N)]
sellquantity_result = [pulp.value(sellquantity[n]) for n in range(N)]
stock_result = [pulp.value(stock[n]) for n in range(N)]

# Prepare output data
output_data = {
    "buyquantity": buyquantity_result,
    "sellquantity": sellquantity_result,
    "stock": stock_result
}

# Print output results
print(json.dumps(output_data))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')