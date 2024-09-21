import pulp

# Data from the provided JSON
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 0.01,  # Convert percentage to decimal
    'TaxRate': 0.15,  # Convert percentage to decimal
    'K': 5000
}

# Extract data
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Initialize the problem
problem = pulp.LpProblem("Investment_Portfolio", pulp.LpMaximize)

# Decision variables: x_i is the number of shares i sold
x = [pulp.LpVariable(f'x{i}', lowBound=0) for i in range(N)]

# Objective function: Maximize the expected value of the portfolio
objective = pulp.lpSum((Bought[i] - x[i]) * FuturePrice[i] for i in range(N))
problem += objective

# Constraints
# Non-negativity is already ensured by LpVariable lowBound
# Cannot sell more than bought
for i in range(N):
    problem += x[i] <= Bought[i], f"Cannot_sell_more_than_bought_{i}"

# Amount raised constraint
amount_raised = pulp.lpSum(
    x[i] * CurrentPrice[i] - x[i] * (CurrentPrice[i] - BuyPrice[i]) * TaxRate - x[i] * CurrentPrice[i] * TransactionRate
    for i in range(N)
)
problem += amount_raised >= K, "Amount_raised_constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')