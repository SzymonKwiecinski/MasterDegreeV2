import pulp
import json

# Input data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extracting parameters from the data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Define the problem
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

# Define decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective function: Maximize the expected value of the portfolio
expected_portfolio_value = sum((futurePrice[i] * (bought[i] - sell[i])) for i in range(N))
problem += expected_portfolio_value, "Total_Expected_Value"

# Constraints: Raise at least K net of transaction costs and taxes
net_amounts = [(currentPrice[i] * sell[i]) * (1 - transactionRate) -
                ((currentPrice[i] * sell[i]) - (buyPrice[i] * sell[i])) * taxRate
                for i in range(N)]
problem += sum(net_amounts) >= K, "Net_Amount_Required"

# Solve the problem
problem.solve()

# Output results
sell_shares = [sell[i].varValue for i in range(N)]

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output format
result = {"sell": sell_shares}
print(json.dumps(result))