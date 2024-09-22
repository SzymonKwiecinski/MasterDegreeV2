import pulp
import json

# Input data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Unpack data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Create LP problem
problem = pulp.LpProblem("Investor_Stock_Selling_Problem", pulp.LpMaximize)

# Create variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

# Objective function: Maximize the expected value of the portfolio next year
expected_value = sum((futurePrice[i] * (bought[i] - sell[i]) - buyPrice[i] * bought[i]) for i in range(N))
problem += expected_value, "Maximize_Expected_Portfolio_Value"

# Constraints: Net amount raised after transaction costs and taxes must be >= K
net_amount = sum((currentPrice[i] * sell[i] * (1 - transactionRate) - 
                  (currentPrice[i] * sell[i] - buyPrice[i] * sell[i]) * taxRate) for i in range(N))

problem += net_amount >= K, "Required_Net_Amount"

# Solve the problem
problem.solve()

# Output the results
sell_shares = [pulp.value(sell[i]) for i in range(N)]
output = {"sell": sell_shares}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')