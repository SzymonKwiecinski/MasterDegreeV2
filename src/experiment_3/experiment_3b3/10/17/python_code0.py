import pulp

# Extracting data
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0,
    'TaxRate': 15.0,
    'K': 5000
}

N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Initialize the problem
problem = pulp.LpProblem("Stock_Selling_Decision", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(FuturePrice[i] * (Bought[i] - sell[i]) for i in range(N))

# Constraints
# Capital Gains and Transaction Costs
problem += pulp.lpSum(
    CurrentPrice[i] * sell[i] * (1 - TransactionRate / 100) -
    BuyPrice[i] * sell[i] * (1 - TaxRate / 100) for i in range(N)
) >= K

# Non-Negativity and Maximum Shares Constraint
for i in range(N):
    problem += sell[i] <= Bought[i]

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Vector of shares to sell
sell_result = [pulp.value(sell[i]) for i in range(N)]
print("Sell shares:", sell_result)