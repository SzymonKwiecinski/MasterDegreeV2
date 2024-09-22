import pulp

# Parse the input data
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
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100.0
taxRate = data['TaxRate'] / 100.0
K = data['K']

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Define the decision variables
sell = [pulp.LpVariable(f'sell_{i}', 0, bought[i], cat='Continuous') for i in range(N)]

# Define the objective function
expected_value_next_year = pulp.lpSum(
    [(bought[i] - sell[i]) * futurePrice[i] for i in range(N)]
)
problem += expected_value_next_year

# Define the constraint to raise at least K money
capital_gain = [
    sell[i] * (currentPrice[i] - buyPrice[i]) for i in range(N)
]
transaction_cost = [
    sell[i] * currentPrice[i] * transactionRate for i in range(N)
]
net_amount_received = [
    sell[i] * currentPrice[i] - transaction_cost[i] - capital_gain[i] * taxRate
    for i in range(N)
]
problem += pulp.lpSum(net_amount_received) >= K

# Solve the problem
problem.solve()

# Prepare the output
sell_shares = [pulp.value(sell[i]) for i in range(N)]

# Print the output in the desired format
output_data = {"sell": sell_shares}
print(output_data)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')