import pulp
import json

data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Extracting data
P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', lowBound=0, upBound=1, cat='Binary')

# Objective function
net_income = pulp.lpSum((prices[i] * production[i] - costs[i] * production[i] - (prices[i] * production[i] * invest_percentage[i])) for i in range(P))
                        - upgrade_cost * upgrade

problem += net_income

# Constraints
# Available cash constraint
problem += pulp.lpSum(costs[i] * production[i] for i in range(P)) + upgrade_cost * upgrade <= cash, "Cash_Constraint"

# Machine hours constraint
problem += pulp.lpSum(hours[i] * production[i] for i in range(P)) <= available_hours + upgrade_hours * upgrade, "Hours_Constraint"

# Solve the problem
problem.solve()

# Output results
net_income_value = pulp.value(problem.objective)
production_values = [pulp.value(production[i]) for i in range(P)]
upgrade_value = pulp.value(upgrade) == 1

output = {
    "net_income": net_income_value,
    "production": production_values,
    "upgrade": upgrade_value,
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')