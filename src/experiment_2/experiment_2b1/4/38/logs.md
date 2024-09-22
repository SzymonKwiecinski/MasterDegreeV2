# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A small computer manufacturing company forecasts the demand over the next \var{n}-th month to be \var{demand_{n}}.
- These demands must be satisfied and can not be shorted.
- In any month it can produce at most \var{max_regular_amount} units, using regular production, at a cost of \var{cost_regular} dollars per unit. 
- By using overtime, it can produce additional units at \var{cost_overtime} dollars per unit. 
- The firm can store units from month to month at a cost of \var{store_cost} dollars per unit per month. 

INPUT FORMAT:

{
	"demand": [demand_{n} for n in 1,...,N],
	"max_regular_amount": max_regular_amount,
	"cost_regular": cost_regular,
	"cost_overtime": cost_overtime,
	"store_cost": store_cost
}


OBJECTIVE: Formulate the problem of determining the production schedule that minimizes the cost.

OUTPUT INFO:

- \var{reg_quant} represents the quantity of products produced using regular production in each future month
- \var{over_quant} represents the quantity of products produced using overtime production in each future month

OUTPUT FORMAT:

{
	"reg_quant": [reg_quant_{n} for n in 1,...,N]
	"over_quant": [over_quant_{n} for n in 1,...,N]
}
</DESCRIPTION>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

#### Unpacking data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
n_months = len(demand)

#### Create the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{i}', lowBound=0, upBound=max_regular_amount, cat='Continuous') for i in range(n_months)]
over_quant = [pulp.LpVariable(f'over_quant_{i}', lowBound=0, cat='Continuous') for i in range(n_months)]
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(n_months)]

#### Objective function
problem += pulp.lpSum(cost_regular * reg_quant[i] + cost_overtime * over_quant[i] + store_cost * inventory[i] for i in range(n_months))

#### Constraints
for i in range(n_months):
    if i == 0:
        problem += reg_quant[i] + over_quant[i] - demand[i] + inventory[i] == 0
    else:
        problem += reg_quant[i] + over_quant[i] + inventory[i-1] - demand[i] + inventory[i] == 0

for i in range(n_months):
    if i > 0:
        problem += inventory[i] >= 0

#### Solve the problem
problem.solve()

#### Extract the results
reg_quant_values = [pulp.value(var) for var in reg_quant]
over_quant_values = [pulp.value(var) for var in over_quant]

#### Output the results
output = {
    "reg_quant": reg_quant_values,
    "over_quant": over_quant_values
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

