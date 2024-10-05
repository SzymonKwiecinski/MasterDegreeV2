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

#### Load data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}
demands = data['demand']
max_regular = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
months = len(demands)

#### Define LP problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Define decision variables
reg_prod = [pulp.LpVariable(f'reg_prod_{i}', lowBound=0, upBound=max_regular, cat='Continuous') for i in range(months)]
over_prod = [pulp.LpVariable(f'over_prod_{i}', lowBound=0, cat='Continuous') for i in range(months)]
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(months + 1)]

#### Initial inventory is zero
problem += inventory[0] == 0

#### Add demand satisfaction constraints
for i in range(months):
    if i == 0:
        problem += reg_prod[i] + over_prod[i] == demands[i] + inventory[i+1]
    else:
        problem += reg_prod[i] + over_prod[i] + inventory[i] == demands[i] + inventory[i+1]

#### Define the objective function: minimize total cost
total_cost = (
    pulp.lpSum(cost_regular * reg_prod[i] for i in range(months)) +
    pulp.lpSum(cost_overtime * over_prod[i] for i in range(months)) +
    pulp.lpSum(store_cost * inventory[i+1] for i in range(months))
)

problem += total_cost

#### Solve the problem
problem.solve()

#### Prepare output
reg_quant = [pulp.value(reg_prod[i]) for i in range(months)]
over_quant = [pulp.value(over_prod[i]) for i in range(months)]

output = {
    "reg_quant": reg_quant,
    "over_quant": over_quant
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

