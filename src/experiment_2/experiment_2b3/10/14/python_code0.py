import pulp

# Problem data
data = {
    "P": 2, 
    "Cash": 3000, 
    "Hour": [2, 6], 
    "Cost": [3, 2], 
    "Price": [6, 5], 
    "InvestPercentage": [0.4, 0.3], 
    "UpgradeHours": 2000, 
    "UpgradeCost": 400, 
    "AvailableHours": 2000
}

P = data["P"]
cash = data["Cash"]
hour = data["Hour"]
cost = data["Cost"]
price = data["Price"]
invest_percentage = data["InvestPercentage"]
upgrade_hours = data["UpgradeHours"]
upgrade_cost = data["UpgradeCost"]
available_hours = data["AvailableHours"]

# Create a LP problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable("upgrade", cat="Binary")

# Objective function
net_income = pulp.lpSum([(price[i] - cost[i] - invest_percentage[i] * price[i]) * production[i] for i in range(P)])
problem += net_income

# Constraints
# Machine hours constraint
problem += pulp.lpSum([hour[i] * production[i] for i in range(P)]) <= available_hours + upgrade_hours * upgrade

# Cash constraint
problem += pulp.lpSum([(cost[i] + invest_percentage[i] * price[i]) * production[i] for i in range(P)]) <= cash + upgrade_cost * upgrade

# Solve the problem
problem.solve()

# Prepare the results
result = {
    "net_income": pulp.value(problem.objective),
    "production": [pulp.value(production[i]) for i in range(P)],
    "upgrade": pulp.value(upgrade) == 1
}

print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(result)