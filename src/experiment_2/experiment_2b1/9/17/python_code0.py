import pulp
import json

# Input data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Define the problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, upBound=None)

# Objective function: maximize expected future value of the portfolio
expected_future_value = pulp.lpSum((futurePrice[i] * (bought[i] - sell[i])) for i in range(N))
problem += expected_future_value

# Constraints
# Net amount raised after transaction costs and taxes must be at least K
net_amount = pulp.lpSum(
    ((currentPrice[i] * sell[i]) * (1 - transactionRate) - ((currentPrice[i] * sell[i] - buyPrice[i] * sell[i]) * taxRate)) for i in range(N)
)
problem += net_amount >= K

# Constraints on the number of shares to sell
for i in range(N):
    problem += sell[i] <= bought[i]

# Solve the problem
problem.solve()

# Prepare output
sell_shares = [sell[i].varValue for i in range(N)]
output = {"sell": sell_shares}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')