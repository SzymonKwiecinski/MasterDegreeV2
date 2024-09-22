import pulp
import json

# Input data
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # number of products
N = len(available)  # number of raw materials

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0, upBound=None, cat='Continuous')

# Objective function
profit = pulp.lpSum((prices[j] - costs[j]) * amount[j] for j in range(M))
problem += profit

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i], f"RawMaterialConstraint_{i}"
    
for j in range(M):
    problem += amount[j] <= demands[j], f"DemandConstraint_{j}"

# Solve the problem
problem.solve()

# Extracting results
amounts_list = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output
output_data = {
    "amount": amounts_list,
    "total_profit": total_profit
}

print(json.dumps(output_data))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')