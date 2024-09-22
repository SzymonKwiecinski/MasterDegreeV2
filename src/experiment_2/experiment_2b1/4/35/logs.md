# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- Consider the problem of operating a warehouse, by buying and selling the stock of a certain commodity, in order to maximize profit over a certain length of time, say several periods.
- The warehouse has a fixed capacity \var{capacity}, and there is a cost \var{holding_cost} per unit for holding stock for one period.
- The selling price, \var{price_{n}}$, of the commodity is known to fluctuate over a number of time periods. 
- In any period \var{n} the price holding for purchase is \var{cost_{n}}.
- The warehouse is originally empty and is required to be empty at the end of the last period.

INPUT FORMAT:

{
	"capacity": capacity,
	"holding_cost": holding_cost,
	"price", [price_{n} for n in 1,...,N],
	"cost": [cost_{n} for n in 1,...,N]
}


OBJECTIVE: Determine the amount of buying and selling in each period to maximize the profit over the months

OUTPUT INFO:

- \var{buyquantity} represents the amount of buying in each period
- \var{sellquantity} represents the amount of selling in each period
- \var{stock} represents the stock in each period, excluding the intial stock

OUTPUT FORMAT:

{
	"buyquantity": [buyquantity_{n} for n in 1,...,N],
	"sellquantity": [sellquantity_{n} for n in 1,...,N],
	"stock": [stock_{n} for n in 1,...,N]
}
</DESCRIPTION>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

#### Extracting the parameters from the input data
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

#### Creating the optimization problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

#### Decision variables
buyquantities = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0, cat='Continuous')
sellquantities = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0, cat='Continuous')
stocks = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

#### Objective function: Maximize profit
profit = pulp.lpSum((prices[n] * sellquantities[n] - costs[n] * buyquantities[n] - holding_cost * stocks[n]) for n in range(N))
problem += profit

#### Constraints
#### Capacity constraint
problem += (pulp.lpSum(buyquantities[n] for n in range(N)) <= capacity), "Capacity"

#### Stock balance for each period
for n in range(N):
    if n == 0:
        problem += (stocks[n] == buyquantities[n] - sellquantities[n]), f"Stock_Balance_{n}"
    else:
        problem += (stocks[n] == stocks[n-1] + buyquantities[n] - sellquantities[n]), f"Stock_Balance_{n}"

#### Final stock should be zero
problem += (stocks[N-1] == 0), "Final_Stock_Zero"

#### Solving the problem
problem.solve()

#### Storing the results
solution = {
    "buyquantity": [buyquantities[n].varValue for n in range(N)],
    "sellquantity": [sellquantities[n].varValue for n in range(N)],
    "stock": [stocks[n].varValue for n in range(N)]
}

#### Output the result
print(json.dumps(solution))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

