import pulp

# Input data
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

# Extracting values from data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Define the problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Define decision variables
sell = [pulp.LpVariable(f"sell_{i}", lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective function: Maximize expected portfolio value next year after selling shares
profit_from_sales = [sell[i] * current_price[i] * (1 - transaction_rate - tax_rate * (current_price[i] - buy_price[i]) / current_price[i]) for i in range(N)]
expected_portfolio_value = sum(profit_from_sales) + sum([(bought[i] - sell[i]) * future_price[i] for i in range(N)])

problem += expected_portfolio_value

# Constraints: The money raised after costs must be at least K
money_raised = sum(profit_from_sales)
problem += money_raised >= K, "Money_Raised_Constraint"

# Solve the problem
problem.solve()

# Prepare the result
sell_result = [pulp.value(sell[i]) for i in range(N)]

# Print the output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print({"sell": sell_result})