# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate this problem as a Linear Programming (LP) model, let's define the decision variables, objective function, and constraints based on the given information.

######### Decision Variables:
- Let \( x_k \) be the amount of food type \( k \) to purchase.

######### Objective Function:
- We want to minimize the total cost of purchasing the foods, which can be expressed as:
  \[
  \min \sum_{k=1}^{K} \text{price}_k \cdot x_k
  \]

######### Constraints:
- Nutritional requirements: For each nutrient \( m \), the total units of that nutrient provided by the combination of foods should meet the daily demand:
  \[
  \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m \quad \text{for each } m = 1, \ldots, M
  \]

- Non-negativity constraint: The quantity of each food must be non-negative:
  \[
  x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
  \]

Here's how this LP model can be written in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model for Balanced Diet:}

\begin{align*}
\text{Minimize:} \quad & \sum_{k=1}^{K} \text{price}_k \cdot x_k \\
\text{Subject to:} \quad & \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m, \quad \text{for } m = 1, \ldots, M \\
& x_k \geq 0, \quad \text{for } k = 1, \ldots, K
\end{align*}

\end{document}
```

This LaTeX code provides a mathematical description of the optimization problem where the goal is to find the quantity of each food type \( x_k \) that minimizes the total cost while meeting the nutritional demands.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model for Balanced Diet:}

\begin{align*}
\text{Minimize:} \quad & \sum_{k=1}^{K} \text{price}_k \cdot x_k \\
\text{Subject to:} \quad & \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m, \quad \text{for } m = 1, \ldots, M \\
& x_k \geq 0, \quad \text{for } k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

#### Parameters
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

#### Number of food items and nutrients
K = len(prices)
M = len(demands)

#### Problem
problem = pulp.LpProblem('Balanced_Diet', pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K))

#### Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demands[m]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

