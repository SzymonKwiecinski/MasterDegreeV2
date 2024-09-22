import pulp
import json

data = {'available': [40, 50, 80], 
        'carbon': [3, 4, 3.5], 
        'nickel': [1, 1.5, 1.8], 
        'alloy_prices': [380, 400, 440], 
        'steel_prices': [650, 600], 
        'carbon_min': [3.6, 3.4], 
        'nickel_max': [1.5, 1.7]}

# Constants
A = len(data['available'])  # number of alloys
S = len(data['steel_prices'])  # number of steel types

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0)  # amount of each alloy used for each steel
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)  # total amount of each steel produced

# Objective Function
profit = pulp.lpSum(
    (data['steel_prices'][s] * total_steel[s] - pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a][s] for a in range(A))) 
    for s in range(S)
)
problem += profit

# Constraints for alloy availability
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= data['available'][a], f"AlloyAvailability_{a}"

# Constraints for carbon and nickel requirements
for s in range(S):
    problem += (
        pulp.lpSum(alloy_amount[a][s] * data['carbon'][a] for a in range(A)) >= data['carbon_min'][s] * total_steel[s],
        f"CarbonRequirement_{s}"
    )
    problem += (
        pulp.lpSum(alloy_amount[a][s] * data['nickel'][a] for a in range(A)) <= data['nickel_max'][s] * total_steel[s],
        f"NickelRequirement_{s}"
    )

# Constraint for alloy 1 usage
for s in range(S):
    problem += alloy_amount[0][s] <= 0.4 * total_steel[s], f"Alloy1_Usage_{s}"

# Solve the problem
problem.solve()

# Prepare output
alloy_use = [[pulp.value(alloy_amount[a][s]) for a in range(A)] for s in range(S)]
total_steel_output = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_output,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')