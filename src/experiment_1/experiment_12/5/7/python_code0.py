import pulp

# Data from the JSON
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

# Extract data
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Create the LP maximization problem
problem = pulp.LpProblem("Maximize_Future_Investment_Value", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

# Objective function
problem += pulp.lpSum((Bought[i] - x[i]) * FuturePrice[i] for i in range(N)), "Total_Expected_Future_Value"

# Constraints
# Amount raised constraint
problem += pulp.lpSum([
    x[i] * CurrentPrice[i] - 
    x[i] * (CurrentPrice[i] - BuyPrice[i]) * (TaxRate / 100) - 
    x[i] * CurrentPrice[i] * (TransactionRate / 100)
    for i in range(N)
]) >= K, "Minimum_Amount_Raised"

# Solve the problem
problem.solve()

# Print the optimal value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')