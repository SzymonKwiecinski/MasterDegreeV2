import pulp
import json

# Input data
data = {
    'n_mines': 4, 
    'n_maxwork': 3, 
    'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 
    'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 
    'quality': [1.0, 0.7, 1.5, 0.5], 
    'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 
    'price': 10, 
    'discount': 0.1
}

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Create the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", (range(n_mines), range(len(requiredquality))), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(n_mines), range(len(requiredquality))), lowBound=0)

# Objective function
profit = pulp.lpSum((price * pulp.lpSum(amount[k][i] for k in range(n_mines)) * (1 / ((1 + discount) ** i))) -
                    pulp.lpSum(royalty[k] * isoperated[k][i] for k in range(n_mines)))
problem += profit, "Total_Profit"

# Constraints
# Each year, a maximum of n_maxwork mines can be operated
for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork, f"Max_Worked_Mines_Year_{i}"

# Ensuring the quality of blended ore meets the required quality
for i in range(len(requiredquality)):
    problem += pulp.lpSum(quality[k] * amount[k][i] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[k][i] for k in range(n_mines)), f"Quality_Requirement_Year_{i}"

# Amount produced cannot exceed the limit and must be consistent with isoperated
for i in range(len(requiredquality)):
    for k in range(n_mines):
        problem += amount[k][i] <= limit[k] * isoperated[k][i], f"Amount_Limit_Mine_{k}_Year_{i}"

# Solve the problem
problem.solve()

# Output results
isoperated_result = [[pulp.value(isoperated[k][i]) for i in range(len(requiredquality))] for k in range(n_mines)]
amount_result = [[pulp.value(amount[k][i]) for i in range(len(requiredquality))] for k in range(n_mines)]

output = {
    "isoperated": isoperated_result,
    "amount": amount_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')