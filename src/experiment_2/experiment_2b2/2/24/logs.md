# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- A mining company is going to continue operating in a certain area for the next years. 
- There are \var{n_mines} mines in this area, but it can operate at most \var{n_maxwork} in any one year. 
- Although a mine may not operate in a certain year, it is still necessary to keep it ‘open’, in the sense that royalties are payable, if it be operated in a future year. 
- Clearly, if a mine is not going to be worked again, it can be permanently closed down and no more royalties need be paid. 
- The yearly royalties payable on each mine kept ‘open’ is \var{royalty_{k}} for mine \var{k}.
- There is an upper limit to the amount of ore, which can be extracted from each mine in a year. 
- The upper limit for mine \var{k} is \var{limit_{k}}.
- The ore from the different mines is of varying quality.
- This quality is measured on a scale so that blending ores together results in a linear combination of the quality measurements, for example, if equal quantities of two ores were combined, the resultant ore would have a quality measurement half way between
that of the ingredient ores. 
- The quality of ore from mine \var{k} is \var{quality_{k}}.
- In each year, it is necessary to combine the total outputs from each mine to produce a blended ore of exactly some stipulated quality.
- In year \var{i}, the required quality is \var{requiredquality_{i}}.
- The final blended ore sells for \var{price} ton each year. 
- Revenue and expenditure for future years must be discounted at a rate of \var{discount} per annum.

INPUT FORMAT:

{
    "n_mines": n_mines,
    "n_maxwork": n_maxwork,
    "royalty": [royalty_{k} for k in 1,...,K],
    "limit": [limit_{k} for k in 1,...,K],
    "quality": [quality_{k} for k in 1,...,K],
    "requiredquality": [requiredquality_{i} for i in 1,...,I],
    "price": price,
    "discount": discount
}


OBJECTIVE: To maximize profit, which mines should be operated each year and how much should they produce?

OUTPUT INFO:

- \var{isoperated} represents whether each mine is operated in each year
- \var{amount} represents the amount of ore produced by each mine in each year

OUTPUT FORMAT:

{
    "isoperated": [[isoperated_{k, i} for i in 1,...,I] for k in 1,...K]
    "amount": [[amount_{k, i} for i in 1,...,I] for k in 1,...K]
}
</DESCRIPTION>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value
from math import pow

#### Data
data = {
    'n_mines': 4,
    'n_maxwork': 3,
    'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    'quality': [1.0, 0.7, 1.5, 0.5],
    'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0],
    'price': 10,
    'discount': 0.1
}

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

n_years = len(requiredquality)

#### Problem
problem = LpProblem("Maximize_Profit", LpMaximize)

#### Decision variables
isoperated = [[LpVariable(f"isoperated_{k}_{i}", cat='Binary') for i in range(n_years)] for k in range(n_mines)]
amount = [[LpVariable(f"amount_{k}_{i}", lowBound=0) for i in range(n_years)] for k in range(n_mines)]

#### Objective
discounted_revenue = lpSum([
    price * lpSum(amount[k][i] for k in range(n_mines)) / pow(1 + discount, i + 1) for i in range(n_years)
])

discounted_royalty = lpSum([
    lpSum(isoperated[k][i] * royalty[k] for k in range(n_mines)) / pow(1 + discount, i + 1) for i in range(n_years)
])

profit = discounted_revenue - discounted_royalty
problem += profit

#### Constraints
for i in range(n_years):
    #### Quality constraint for each year
    problem += lpSum(amount[k][i] * quality[k] for k in range(n_mines)) == lpSum(amount[k][i] for k in range(n_mines)) * requiredquality[i]

    #### Max number of mines operated per year
    problem += lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork

    for k in range(n_mines):
        #### Do not exceed limit of each mine
        problem += amount[k][i] <= limit[k] * isoperated[k][i]

        #### If in any year a mine is operated, it must be operated in previous years or open
        if i > 0:
            problem += isoperated[k][i] >= isoperated[k][i - 1]

#### Solve the problem
problem.solve()

#### Results
solution = {
    "isoperated": [[int(isoperated[k][i].varValue) for i in range(n_years)] for k in range(n_mines)],
    "amount": [[amount[k][i].varValue for i in range(n_years)] for k in range(n_mines)]
}

print(solution)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')
```

