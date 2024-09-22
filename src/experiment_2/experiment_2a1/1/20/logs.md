# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- An engineering factory makes several products on the machines, and the number of machine \var{m} the factory has is \var{num_{m}}.
- Each product \var{k} yields \var{profit_{k}} to profit (defined as £/unit selling price minus cost of raw materials).
- The unit production times (hours) product \var{k} requires on machine \var{m} is \var{time_{k, m}}
- In the present month (January) and several subsequent months, certain machines will be down for maintenance.
- In month \var{i}, the number of machine \var{m} that will be down is \var{maintain_{i, m}}.
- There are marketing limitations on each product in each month. 
- The limitation of product \var{k} in month \var{i} is \var{limit_{k, i}}.
- It is possible to store up to 100 of each product at a time at a cost of \var{store_price} per unit per month. 
- There are no stocks at present, but we should have a stock of \var{keep_quantity} of each type of product at the end of subsequent months.
- The factory works six days a week with \var{n_workhours} hours each day. 
- No sequencing problems need to be considered.
- We can assume that a month has 24 days for convenience.

INPUT FORMAT:

{
    "num_machines": [num_{m} for m in 1,...,M],
    "profit": [profit_{k} for k in 1,...K],
    "time": [[time_{k, m} for m in 1,...,M] for k in 1,...,K],
    "maintain": [[maintain_{i, m} for m in 1,...,M] for i in 1,...,I],
    "limit": [[limit_{k, i} for i in 1,...,I] for k in 1,...,K],
    "store_price": store_price,
    "keep_quantity": keep_quantity,
    "n_workhours": n_workhours
}

OBJECTIVE: What selling, storing and manufacturing policy should the company pursue in order to maximize profit?

OUTPUT INFO:

- \var{sell} represents the amount of selling quantity of each product in each month
- \var{manufacture} represents the amount of manufactured products in each month
- \var{storage} represents the storage of each product in each month

OUTPUT FORMAT:

{
    "sell": [[sell_{k, i} for k in 1,...,K] for i in 1,...I],
    "manufacture": [[manufacture_{k, i} for k in 1,...,K] for i in 1,...I],
    "storage": [[storage_{k, i} for k in 1,...,K] for i in 1,...,I]
}

</DESCRIPTION>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3],
        'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0],
                 [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0],
                 [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
        'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0],
                     [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1]],
        'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500],
                  [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300],
                  [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500],
                  [100, 150, 100, 100, 0, 60]],
        'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}

num_products = len(data['profit'])
num_months = len(data['limit'][0])
num_machines = len(data['num_machines'])

#### Create the model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum([data['profit'][k] * sell[k, i] for k in range(num_products) for i in range(num_months)]) - pulp.lpSum([data['store_price'] * storage[k, i] for k in range(num_products) for i in range(num_months)])

#### Constraints
#### Storage balance constraints
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += storage[k, i] == data['keep_quantity'] + manufacture[k, i] - sell[k, i], f"Storage_Balance_Product_{k}_Month_{i}"
        else:
            problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i], f"Storage_Balance_Product_{k}_Month_{i}"

#### Production time constraints
for i in range(num_months):
    for m in range(num_machines):
        available_hours = data['n_workhours'] * (24 - sum(data['maintain'][i][m] for i in range(num_months)))
        problem += pulp.lpSum([data['time[k][m]'] * manufacture[k, i] for k in range(num_products)]) <= available_hours, f"Time_Constraint_Machine_{m}_Month_{i}"

#### Selling limit constraints
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k, i] <= data['limit'][k][i], f"Selling_Limit_Product_{k}_Month_{i}"

#### keep_quantity constraint for each product at the end of last month
for k in range(num_products):
    problem += storage[k, num_months - 1] >= data['keep_quantity'], f"Keep_Quantity_Product_{k}"

#### Solve the problem
problem.solve()

#### Output results
sell_result = [[sell[k, i].varValue for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[manufacture[k, i].varValue for k in range(num_products)] for i in range(num_months)]
storage_result = [[storage[k, i].varValue for k in range(num_products)] for i in range(num_months)]

output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

