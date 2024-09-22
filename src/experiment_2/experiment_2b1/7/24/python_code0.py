import pulp
import json

data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 
        'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 
        'quality': [1.0, 0.7, 1.5, 0.5], 
        'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 
        'price': 10, 'discount': 0.1}

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Create the LP problem
problem = pulp.LpProblem("Mining_Company_Profit_Maximization", pulp.LpMaximize)

# Create decision variables
isoperated = pulp.LpVariable.dicts("isoperated", 
                                     ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), 
                                     0, 1, pulp.LpBinary)

amount = pulp.LpVariable.dicts("amount", 
                                 ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), 
                                 0, None)

# Objective function: Maximize profit
profit = pulp.lpSum((price * amount[k, i] - royalty[k] * isoperated[k, i]) * 
                    (1 / ((1 + discount) ** i)) for k in range(n_mines) for i in range(len(requiredquality)))

problem += profit

# Constraints
# Ensure that the required quality is met
for i in range(len(requiredquality)):
    problem += pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines))

# Limit the amount of ore that can be extracted from each mine
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Limit the number of mines that can be operated
for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

# Solve the problem
problem.solve()

# Preparing output
isoperated_result = [[pulp.value(isoperated[k, i]) for i in range(len(requiredquality))] for k in range(n_mines)]
amount_result = [[pulp.value(amount[k, i]) for i in range(len(requiredquality))] for k in range(n_mines)]

output_result = {
    "isoperated": isoperated_result,
    "amount": amount_result
}

print(json.dumps(output_result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')