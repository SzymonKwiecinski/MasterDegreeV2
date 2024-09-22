import pulp
import json

data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], 
                        [40, 1, 10], 
                        [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Extract data from the input
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create decision variables for the amount of each product to produce
amounts = [pulp.LpVariable(f'amount_{j}', lowBound=0, upBound=demand) for j, demand in enumerate(demands)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amounts[j] for j in range(M)])
problem += profit

# Constraints for each raw material
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i]

# Solve the problem
problem.solve()

# Prepare the results
amounts_result = [pulp.value(amount) for amount in amounts]
total_profit = pulp.value(problem.objective)

# Output in the required format
output = {
    "amount": amounts_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')