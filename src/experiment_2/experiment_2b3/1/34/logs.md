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
To solve this Linear Programming problem using the Pulp library in Python, we'll need to set up the problem as described: minimizing the total cost of food items while meeting the required nutritional demands. Here's the implementation:

```python
import pulp

#### Parse the input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

#### Extract data components
prices = data['price']
demands = data['demand']
nutritions = data['nutrition']

#### Number of foods and nutrients
num_foods = len(prices)
num_nutrients = len(demands)

#### Create the LP problem instance
problem = pulp.LpProblem("Balanced_Diet_Problem", pulp.LpMinimize)

#### Define decision variables for the quantity of each food
quantity_vars = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_foods)]

#### Objective function: minimize the total price
total_cost = pulp.lpSum([prices[k] * quantity_vars[k] for k in range(num_foods)])
problem += total_cost

#### Constraints: meet the demand for each nutrient
for m in range(num_nutrients):
    nutrient_constraint = pulp.lpSum([nutritions[k][m] * quantity_vars[k] for k in range(num_foods)]) >= demands[m]
    problem += nutrient_constraint

#### Solve the problem
problem.solve()

#### Collect results
result_quantity = [pulp.value(quantity_vars[k]) for k in range(num_foods)]

#### Prepare output
output = {"quantity": result_quantity}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

This code sets up a Linear Programming model to minimize the purchase cost of foods while satisfying the necessary nutritional demands. It uses Pulp to define decision variables, constraints, and the objective function, then solves the problem and outputs both the solution and the objective value.

