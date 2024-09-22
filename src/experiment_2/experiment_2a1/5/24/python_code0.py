import pulp
import json

# Input data in JSON format
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

# Problem parameters
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
isoperated = pulp.LpVariable.dicts("isoperated", (range(n_mines), range(len(requiredquality))), cat='Binary')  # 1 if mine is operated, 0 otherwise
amount = pulp.LpVariable.dicts("amount", (range(n_mines), range(len(requiredquality))), lowBound=0)  # Amount of ore produced

# Objective function: Maximize profit
profit = pulp.lpSum((price * pulp.lpSum(amount[k][i] for k in range(n_mines)) * (1 / ((1 + discount) ** i))) - 
                    pulp.lpSum(royalty[k] * isoperated[k][i] for k in range(n_mines)) 
                    for i in range(len(requiredquality)))
problem += profit

# Constraints
# Each year's total quality must meet the required quality
for i in range(len(requiredquality)):
    problem += pulp.lpSum(amount[k][i] * quality[k] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[k][i] for k in range(n_mines))

# Limit the amount of ore extracted from each mine to its upper limit
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k][i] <= limit[k] * isoperated[k][i]

# Limit the number of mines that can operate in any one year
for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork

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