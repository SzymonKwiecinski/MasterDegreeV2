import pulp

# Data
data = {
    'P': 2, 
    'Cash': 3000, 
    'Hour': [2, 6], 
    'Cost': [3, 2], 
    'Price': [6, 5], 
    'InvestPercentage': [0.4, 0.3], 
    'UpgradeHours': 2000, 
    'UpgradeCost': 400, 
    'AvailableHours': 2000
}

P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Define problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(P)]
y = pulp.LpVariable('y', cat='Binary')

# Objective Function
problem += pulp.lpSum([(price[i] * x[i] - cost[i] * x[i] - investPercentage[i] * price[i] * x[i]) for i in range(P)]) - upgradeCost * y, "Net_Income"

# Constraints
problem += pulp.lpSum([hour[i] * x[i] for i in range(P)]) <= availableHours + upgradeHours * y, "Machine_Hours_Constraint"
problem += pulp.lpSum([cost[i] * x[i] for i in range(P)]) <= cash, "Cash_Constraint"

# Solve
problem.solve()

print("Optimization Results:")
for i in range(P):
    print(f"Production of product {i+1}: {x[i].varValue}")

print(f"Upgrade Machine: {'Yes' if y.varValue == 1 else 'No'}")
print(f"Net Income (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")