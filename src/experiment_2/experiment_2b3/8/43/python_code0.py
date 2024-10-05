import pulp

# Input data
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Decision Variables
# amount[j]: the amount of product j to be produced
M = len(data['prices'])
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function: Maximize total profit
profit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit[j] * amount[j] for j in range(M)), "Total_Profit"

# Constraints
# 1. Raw Material Constraints
N = len(data['available'])
for i in range(N):
    problem += pulp.lpSum(data['requirements'][j][i] * amount[j] for j in range(M)) <= data['available'][i], f"Material_{i}_Constraint"

# 2. Demand Constraints
for j in range(M):
    problem += amount[j] <= data['demands'][j], f"Demand_{j}_Constraint"

# Solve
problem.solve()

# Results
amount_produced = [pulp.value(amount[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output
output = {"amount": amount_produced, "total_profit": total_profit}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')