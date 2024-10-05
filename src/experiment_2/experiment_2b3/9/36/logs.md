# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A manufacturer wishes to produce \var{alloy_quant} lb of an alloy that consists of several kinds of metals.
- And by weight, the alloy we want contains a target quantity\var{target_{m}} of metal \var{metal_{m}}.
- Several other kinds of alloys are available at various prices. 
- These alloys can be melted to get the alloy we want.
- Alloy \var{k} has \var{ratio_{k, m}} ratio of \var{metal_{m}} and is sold at price of \var{price_k}.
- Ratio \var{ratio_{k, m}} ranges between 0 and 1.0 and should be properly treated in optimization

INPUT FORMAT:

{
	"alloy_quant": alloy_quant,
	"target": [target_{m} for m in 1,...,M],
	"ratio": [[ratio_{k, m} for m in 1,...,M] for k = 1,...,K],
	"price": [price_{k} for k in 1,...,K]
}

OBJECTIVE: The manufacturer wishes to find the amounts of the various alloys needed and to determine the cheapest combination.

OUTPUT INFO:

- \var{amount} represents the quantity of each alloy we buy

OUTPUT FORMAT:

{
	"amount": [amount_{k} for k in 1,...,K]
}
</DESCRIPTION>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

#### Parse the input data from JSON
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)  #### Number of available alloys
M = len(target)  #### Number of metals

#### Create the LP problem instance
problem = LpProblem("Alloy_Optimization", LpMinimize)

#### Decision variables: amount of each alloy to purchase
amount_vars = [LpVariable(f"amount_{k}", lowBound=0) for k in range(K)]

#### Objective function: Minimize the total cost of alloys
problem += lpSum(prices[k] * amount_vars[k] for k in range(K)), "Total_Cost"

#### Constraint: The sum of all alloys should equal the required alloy quantity
problem += lpSum(amount_vars) == alloy_quant, "Total_Alloy_Quantity"

#### Constraints: Achieve the target composition of metals
for m in range(M):
    problem += lpSum(ratios[k][m] * amount_vars[k] for k in range(K)) == target[m], f"Target_Metal_{m}"

#### Solve the problem
problem.solve()

#### Extract the results
amounts = [amount_vars[k].varValue for k in range(K)]

solution = {
    "amount": amounts
}

print(solution)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')
```

