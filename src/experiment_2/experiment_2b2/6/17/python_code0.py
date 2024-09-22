import pulp

# Transform the input data into variables
data = {
    "N": 3,
    "Bought": [100, 150, 80],
    "BuyPrice": [50, 40, 30],
    "CurrentPrice": [60, 35, 32],
    "FuturePrice": [65, 44, 34],
    "TransactionRate": 1.0,
    "TaxRate": 15.0,
    "K": 5000
}

N = data["N"]
Bought = data["Bought"]
BuyPrice = data["BuyPrice"]
CurrentPrice = data["CurrentPrice"]
FuturePrice = data["FuturePrice"]
TransactionRate = data["TransactionRate"] / 100
TaxRate = data["TaxRate"] / 100
K = data["K"]

# Define the problem
problem = pulp.LpProblem("Investor_Portfolio", pulp.LpMaximize)

# Define decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

# Objective function: Maximize the expected value of the portfolio next year
expected_value = pulp.lpSum((Bought[i] - sell[i]) * FuturePrice[i] for i in range(N))
problem += expected_value

# Add the financial constraints
# Constraint: Amount raised must be at least K, considering transaction costs and taxes
price_after_transaction = [CurrentPrice[i] * (1 - TransactionRate) for i in range(N)]
capital_gain = [pulp.lpSum((CurrentPrice[i] - BuyPrice[i]) * sell[i]) for i in range(N)]
tax_on_capital_gain = [TaxRate * capital_gain[i] for i in range(N)]
net_amount_received = [pulp.lpSum(price_after_transaction[i] * sell[i] - tax_on_capital_gain[i]) for i in range(N)]

problem += (pulp.lpSum(net_amount_received) >= K, "Net_Amount_Required")

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "sell": [pulp.value(sell[i]) for i in range(N)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')