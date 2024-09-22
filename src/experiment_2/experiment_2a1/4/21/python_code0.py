import pulp
import json

# Input data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0],
             [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0],
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [1, 1, 1, 1, 1],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500],
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300],
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500],
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Variables
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])
profit = data['profit']
time = data['time']
down = data['down']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
working_hours_per_month = 24 * 6 * 2  # Total working hours in a month

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(num_machines), range(num_months)), lowBound=0, upBound=1, cat='Binary')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] for k in range(num_products) for i in range(num_months)) - \
            pulp.lpSum(store_price * storage[k][i] for k in range(num_products) for i in range(num_months)), "Total_Profit"

# Constraints
for i in range(num_months):
    for k in range(num_products):
        # Selling limit
        problem += sell[k][i] <= limit[k][i], f"Product_{k}_Limit_Month_{i}"

        # Maintain production capacity
        available_hours = working_hours_per_month - sum(down[m] * maintain[m][i] for m in range(num_machines)) * n_workhours
        problem += (pulp.lpSum(manufacture[k][i] * time[k][m] for m in range(num_machines)) <= available_hours), \
                    f"Production_Hours_Constraint_{i}")

        # Storage constraint
        if i == 0:
            problem += storage[k][i] == keep_quantity, f"Storage_Initial_Condition_{k}"
        else:
            problem += storage[k][i] == storage[k][i-1] + manufacture[k][i-1] - sell[k][i-1] + keep_quantity, \
                        f"Storage_Condition_{k}_{i}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "sell": [[sell[k][i].varValue for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[manufacture[k][i].varValue for k in range(num_products)] for i in range(num_months)],
    "storage": [[storage[k][i].varValue for k in range(num_products)] for i in range(num_months)],
    "maintain": [[maintain[m][i].varValue for m in range(num_machines)] for i in range(num_products)]
}

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')