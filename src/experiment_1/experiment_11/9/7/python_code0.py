import pulp

# Data extracted from the provided JSON format
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

# Parameters
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Investor_Portfolio_Value", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("shares_sold", range(N), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((Bought[i] - x[i]) * FuturePrice[i] for i in range(N)), "Total_Expected_Value"

# Constraints
# Non-negativity constraint (automatically handled by lowBound=0 in the variable definition)

# Cannot sell more than bought
for i in range(N):
    problem += x[i] <= Bought[i], f"Cannot_sell_more_than_bought_{i}"

# Amount raised constraint
problem += pulp.lpSum(
    x[i] * CurrentPrice[i] - x[i] * (CurrentPrice[i] - BuyPrice[i]) * (TaxRate / 100) - x[i] * CurrentPrice[i] * (TransactionRate / 100)
    for i in range(N)
) >= K, "Amount_raised_constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')