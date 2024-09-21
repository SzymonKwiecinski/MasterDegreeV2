import pulp

# Data input
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

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Shares_Sold", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum((Bought[i] - x[i]) * FuturePrice[i] for i in range(N))

# Constraints
# Non-negativity constraint is inherently handled by lowBound=0 in the variable definition
for i in range(N):
    problem += x[i] <= Bought[i], f"Cannot sell more than bought constraint for share {i+1}"

# Amount raised constraint
problem += (pulp.lpSum(x[i] * CurrentPrice[i] - 
                       x[i] * (CurrentPrice[i] - BuyPrice[i]) * (TaxRate / 100) - 
                       x[i] * CurrentPrice[i] * (TransactionRate / 100) for i in range(N)) 
                      >= K, "Amount_Raised_Constraint")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')