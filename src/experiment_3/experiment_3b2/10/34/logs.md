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
To model this problem, we will establish a linear programming formulation. We need to minimize the cost of purchasing foods while ensuring that the nutritional requirements are met.

Let's denote:

- \( x_k \) as the quantity of food \( k \) to purchase.

Given input:

- \( \text{price}_k \) is the price per unit of food \( k \).
- \( \text{demand}_m \) is the minimum number of units of nutrient \( m \) required.
- \( \text{nutri}_{k, m} \) is the amount of nutrient \( m \) in one unit of food \( k \).

The linear programming problem is formulated as follows:

Objective: 
Minimize the total cost of the foods:

\[
\text{Minimize} \quad \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

Subject to nutritional constraints:

\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_k \geq \text{demand}_m \quad \text{for all } m = 1, \ldots, M
\]

And non-negativity constraints on the decision variables:

\[
x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
\]

The corresponding LaTeX code to represent this mathematical formulation is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

Let \( x_k \) be the quantity of food \( k \) to purchase.

\textbf{Objective:}
\[
\text{Minimize} \quad \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_k \geq \text{demand}_m \quad \text{for all } m = 1, \ldots, M
\]

\textbf{Non-negativity constraints:}
\[
x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
\]

\end{document}
```

You can use this linear programming model in an optimization solver to determine the optimal quantities of each food to purchase while minimizing costs and satisfying nutrient requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

Let \( x_k \) be the quantity of food \( k \) to purchase.

\textbf{Objective:}
\[
\text{Minimize} \quad \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_k \geq \text{demand}_m \quad \text{for all } m = 1, \ldots, M
\]

\textbf{Non-negativity constraints:}
\[
x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"price": [1, 2, 3], "demand": [10, 20], "nutrition": [[3, 5], [1, 3], [4, 4]]}')
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

#### Problem setup
K = len(price)  #### Number of food items
M = len(demand)  #### Number of nutritional demands

#### Create the linear programming problem
problem = pulp.LpProblem("Food_Purchase_Problem", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total Cost"

#### Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demand[m], f"Nutritional_Demand_{m+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

