# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We assume that there are available at the market different foods and that the food \var{k} sells at a price \var{price_{k}} per unit. 
- In addition there are several basic nutritional ingredients and, to achieve a balanced diet, each individual must receive at least \var{demand_{m}} units of nutrient \var{m} per day. 
- Finally, we assume that each unit of food \var{k} contains \var{nutri_{k, m}} units of nutrition \var{m}

INPUT FORMAT:

{
	"price": [price_{k} for k in 1,...,K],
	"demand": [demand_{m} for m in 1,...,M],
	"nutrition": [[nutri_{k, m} for m in 1,...,M] for k in 1,...,K]
}


OBJECTIVE: We want to minimize the total prices of the foods to purchase.

OUTPUT INFO:

- \var{quantity} represents the quantity of each food to purchase

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this problem, we'll use the PuLP library in Python to model a Linear Programming problem. The goal is to minimize the total cost of the foods while satisfying the nutritional requirements. Let's create and solve the problem using the given data.

```python
import pulp

#### Read the JSON data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

#### Extract data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

#### Number of foods and nutrients
K = len(price)
M = len(demand)

#### Define the linear programming problem
problem = pulp.LpProblem("Diet_Problem", pulp.LpMinimize)

#### Variables: quantity of each food
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function: Minimize the total cost
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K))

#### Constraints: Satisfy the nutritional demand for each nutrient
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m]

#### Solve the problem
problem.solve()

#### Collect results
result = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

This script sets up the linear programming problem using the PuLP library. It defines the decision variables, objective function, and constraints based on the provided data, and then solves for the optimal quantities of each food type to minimize cost while meeting nutritional requirements.

