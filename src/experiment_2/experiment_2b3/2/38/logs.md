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
To solve this problem, we'll use the PuLP library to create and solve a Linear Programming (LP) model. Let's implement the solution based on the provided data.

```python
import pulp

#### Data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
months = len(demand)

#### Problem
problem = pulp.LpProblem("Production_Schedule", pulp.LpMinimize)

#### Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{i+1}', lowBound=0) for i in range(months)]
over_quant = [pulp.LpVariable(f'over_quant_{i+1}', lowBound=0) for i in range(months)]
storage = [pulp.LpVariable(f'storage_{i+1}', lowBound=0) for i in range(months)]

#### Objective Function
cost = (pulp.lpSum(cost_regular * reg_quant[i] for i in range(months)) +
        pulp.lpSum(cost_overtime * over_quant[i] for i in range(months)) +
        pulp.lpSum(store_cost * storage[i] for i in range(months)))

problem += cost

#### Constraints
for i in range(months):
    #### Meeting demand constraints
    produced = reg_quant[i] + over_quant[i]
    if i == 0:
        problem += (produced + storage[i] == demand[i])
    else:
        problem += (produced + storage[i-1] - storage[i] == demand[i])
    
    #### Regular production limit
    problem += (reg_quant[i] <= max_regular_amount)

#### Solve
problem.solve()

#### Output format
output = {
    "reg_quant": [pulp.value(reg_quant[i]) for i in range(months)],
    "over_quant": [pulp.value(over_quant[i]) for i in range(months)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

This code sets up and solves a linear programming problem that seeks to minimize production and storage costs while meeting monthly demands through regular and overtime production. The solution variables include `reg_quant` for regular production, `over_quant` for overtime production, and `storage` for carrying over inventory. The model considers constraints such as regular production limits and demand satisfaction.

