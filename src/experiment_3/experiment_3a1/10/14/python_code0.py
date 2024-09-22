import pulp

# Data from the provided JSON
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

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Product", range(1, data['P'] + 1), lowBound=0, cat='Continuous')
U = pulp.LpVariable("Upgrade", cat='Binary')

# Objective function
problem += pulp.lpSum(((data['Price'][i-1] - data['Cost'][i-1]) * x[i] - 
                        data['InvestPercentage'][i-1] * (data['Price'][i-1] * x[i]) 
                       for i in range(1, data['P'] + 1))) - U * data['UpgradeCost'], "Total_Net_Income"

# Constraints
problem += pulp.lpSum(data['Cost'][i-1] * x[i] for i in range(1, data['P'] + 1)) <= data['Cash'] - U * data['UpgradeCost'], "Cash_Availability"
problem += pulp.lpSum(data['Hour'][i-1] * x[i] for i in range(1, data['P'] + 1)) <= data['AvailableHours'] + U * data['UpgradeHours'], "Machine_Capacity"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')