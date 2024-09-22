import json
import pulp

# Input data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extracting the data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Create the problem instance
problem = pulp.LpProblem("Investment_Profit_Maximization", pulp.LpMaximize)

# Decision variables: number of shares to sell
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective function: Maximize the future value of the portfolio
expected_future_value = pulp.lpSum((futurePrice[i] * (bought[i] - sell[i])) for i in range(N))
problem += expected_future_value

# Constraints: The net amount raised must be at least K
net_amount = pulp.lpSum(
    (currentPrice[i] * sell[i] * (1 - transactionRate) - 
     (buyPrice[i] * sell[i] * (1 - taxRate))) for i in range(N)
)
problem += net_amount >= K

# Constraints: Cannot sell more shares than bought
for i in range(N):
    problem += sell[i] <= bought[i]

# Solve the problem
problem.solve()

# Prepare the result
sell_shares = [pulp.value(sell[i]) for i in range(N)]

# Output the result
result = {
    "sell": sell_shares
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')