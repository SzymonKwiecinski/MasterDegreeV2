import pulp
import json

# Data input
data = json.loads('{"N": 3, "Bought": [100, 150, 80], "BuyPrice": [50, 40, 30], "CurrentPrice": [60, 35, 32], "FuturePrice": [65, 44, 34], "TransactionRate": 1.0, "TaxRate": 15.0, "K": 5000}')

# Parameters
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

# Create the problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum([
    (future_price[i] * bought[i] - 
     (sell[i] * current_price[i] * (1 + transaction_rate / 100)) - 
     (sell[i] * (current_price[i] - buy_price[i]) * tax_rate / 100))
    ) for i in range(N)
]), "Objective"

# Constraints
problem += (pulp.lpSum([
    (sell[i] * current_price[i] * (1 - transaction_rate / 100) - 
     sell[i] * (current_price[i] - buy_price[i]) * tax_rate / 100)
    for i in range(N)]) >= K, "NetAmountRaised")

for i in range(N):
    problem += (sell[i] <= bought[i], f"MaxSell_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')