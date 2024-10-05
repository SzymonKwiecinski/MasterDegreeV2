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

data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

#### Unpacking data
capacity = data["capacity"]
holding_cost = data["holding_cost"]
prices = data["price"]
costs = data["cost"]
N = len(prices)

#### Define the Linear Programming problem
problem = pulp.LpProblem("Warehouse_Operation_Max_Profit", pulp.LpMaximize)

#### Decision variables
buy_quantity = [pulp.LpVariable(f"buy_quantity_{n}", lowBound=0, cat='Continuous') for n in range(N)]
sell_quantity = [pulp.LpVariable(f"sell_quantity_{n}", lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0, upBound=capacity, cat='Continuous') for n in range(N)]

#### Objective function: Maximize Profit
profit_terms = [prices[n] * sell_quantity[n] - costs[n] * buy_quantity[n] - holding_cost * stock[n] for n in range(N)]
problem += pulp.lpSum(profit_terms), "Total Profit"

#### Constraints
#### Initial and final stock conditions
problem += stock[0] == buy_quantity[0] - sell_quantity[0], "Initial Stock Balance"
problem += stock[N-1] == 0, "Final Stock Zero"

#### Stock balance for each period
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buy_quantity[n] - sell_quantity[n], f"Stock Balance Period {n}"

#### Solve the problem
problem.solve()

#### Results
output = {
    "buyquantity": [pulp.value(buy_quantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sell_quantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

