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

#### Parse the input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
buy = [pulp.LpVariable(f"buy_{n}", lowBound=0) for n in range(N)]
sell = [pulp.LpVariable(f"sell_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0) for n in range(N)]

#### Objective function
profit = pulp.lpSum([(price[n] * sell[n] - cost[n] * buy[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

#### Constraints

#### Initial stock constraint (stock at time 0 is 0)
problem += (stock[0] == buy[0] - sell[0]), "Initial_Stock"

#### Stock capacity constraint and flow balance for each period
for n in range(1, N):
    problem += (stock[n] == stock[n-1] + buy[n] - sell[n]), f"Stock_Balance_{n}"

#### Capacity constraint
for n in range(N):
    problem += (stock[n] <= capacity), f"Capacity_Constraint_{n}"

#### Ending stock must be zero
problem += (stock[N-1] == 0), "Ending_Stock"

#### Solve the problem
problem.solve()

#### Output the results
result = {
    "buyquantity": [pulp.value(buy[n]) for n in range(N)],
    "sellquantity": [pulp.value(sell[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

