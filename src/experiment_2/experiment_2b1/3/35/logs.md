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

#### Extract data from the input
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

#### Define the number of periods
N = len(prices)

#### Create the problem variable
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQty", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("SellQty", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

#### Objective Function: Maximize Profit
profit = pulp.lpSum([(prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

#### Constraints

#### Capacity constraint for each period
for n in range(N):
    if n == 0:
        problem += (stock[n] == buyquantity[n] - sellquantity[n]), f"Stock_Constraint_{n}"
    else:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]), f"Stock_Constraint_{n}"
    
    problem += (buyquantity[n] <= capacity), f"Capacity_Constraint_{n}"
    
#### End of period stock must be zero
problem += (stock[N-1] == 0), "End_Stock_Zero_Constraint"

#### Solve the problem
problem.solve()

#### Prepare the output
output = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Show output
print(json.dumps(output))
```

