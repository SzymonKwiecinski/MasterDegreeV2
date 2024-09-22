# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP
PROBLEM INFO:

- An engineering factory makes several products on the machines, and the number of machine \var{m} the factory has is \var{num_{m}}.
- Each product \var{k} yields \var{profit_{k}} to profit (defined as £/unit selling price minus cost of raw materials).
- The unit production times (hours) product \var{k} requires on machine \var{m} is \var{time_{k, m}}
- In the present month (January) and several subsequent months, certain machines will be down for maintenance.
- Each machine \var{m} has to be down for \var{down_{m}} months for maintenance.
- There are marketing limitations on each product in each month. 
- The limitation of product \var{k} in month \var{i} is \var{limit_{k, i}}.
- It is possible to store up to 100 of each product at a time at a cost of \var{store_price} per unit per month. 
- There are no stocks at present, but it is desired to have a stock of \var{keep_quantity} of each type of product at the end of subsequent months.
- The factory works a six days a week with two shifts of \var{n_workhours} hours each day. 
- No sequencing problems need to be considered.
- We can assume that a month has 24 days for convenience.


INPUT FORMAT:

{
    "num_machines": [num_{m} for m in 1,...,M],
    "profit": [profit_{k} for k in 1,...K],
    "time": [[time_{k, m} for m in 1,...,M] for k in 1,...,K],
    "down": [down_{m} for m in 1,...,M]
    "limit": [[limit_{k, i} for i in 1,...,I] for k in 1,...,K],
    "store_price": store_price,
    "keep_quantity": keep_quantity,
    "n_workhours": n_workhours
}

OBJECTIVE: What maintaining, selling, storing and manufacturing policy should the company pursue in order to maximize profit?

OUTPUT INFO:

- \var{sell} represents the amount of selling quantity of each product in each month
- \var{manufacture} represents the amount of manufactured products in each month
- \var{storage} represents the storage of each product in each month
- \var{maintain} represents the number of machines in each type that are under maintenance in each month

OUTPUT FORMAT:

{
    "sell": [[sell_{k, i} for k in 1,...,K] for i in 1,...I],
    "manufacture": [[manufacture_{k, i} for k in 1,...,K] for i in 1,...I],
    "storage": [[storage_{k, i} for k in 1,...,K] for i in 1,...,I],
    "maintain": [[maintain_{m, k} for m in 1,...,M] for k in 1,...,K]
}

</DESCRIPTION>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [1],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Extract data
num_machines = data['num_machines']
profits = data['profit']
times = data['time']
down_time = data['down'][0]
limits = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
months = len(limits[0])
K = len(profits)
M = len(num_machines)

#### Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(months)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (m for m in range(M)), lowBound=0, cat='Integer')

#### Objective function
problem += pulp.lpSum(profits[k] * sell[k, i] for k in range(K) for i in range(months)) - \
           pulp.lpSum(store_price * storage[k, i] for k in range(K) for i in range(months))

#### Constraints
for i in range(months):
    for k in range(K):
        problem += sell[k, i] <= limits[k][i]
        problem += manufacture[k, i] + storage[k, i-1] - sell[k, i] == storage[k, i] + keep_quantity if i == months - 1 else storage[k, i]  #### keeping last month storage goal
        
        #### Machine time used by manufactured products
        total_time = pulp.lpSum(times[k][m] * manufacture[k, i] for m in range(M))
        max_time = n_workhours * (24 * 6 - down_time)  #### total available hours after maintenance
        problem += total_time <= max_time

#### Maintenance constraints (assuming one machine can only be down for 'down_time' each month)
for m in range(M):
    problem += maintain[m] <= down_time

#### Solve the problem
problem.solve()

#### Prepare output
output = {
    "sell": [[sell[k, i].varValue for k in range(K)] for i in range(months)],
    "manufacture": [[manufacture[k, i].varValue for k in range(K)] for i in range(months)],
    "storage": [[storage[k, i].varValue for k in range(K)] for i in range(months)],
    "maintain": [[maintain[m].varValue for m in range(M)]]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

