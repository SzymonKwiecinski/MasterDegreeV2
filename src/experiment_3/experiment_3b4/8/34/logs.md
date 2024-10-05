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
To formulate the given problem as a linear programming model, we need to consider the decision variables, objective function, and constraints based on the provided information.

######### Decision Variables
Let \( x_k \) represent the quantity of food \( k \) to purchase.

######### Objective Function
We want to minimize the total cost of purchasing the foods. The objective function can be represented as:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \times x_k
\]

######### Constraints
- Nutritional constraints: Each individual must receive at least \(\text{demand}_m\) units of nutrient \( m \) per day, which translates into:
  \[
  \sum_{k=1}^{K} \text{nutri}_{k,m} \times x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M
  \]

- Non-negativity constraints: 
  \[
  x_k \geq 0 \quad \forall k = 1, \ldots, K
  \]

Now, let's present this model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model for Minimizing Food Costs}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_k \) denote the quantity of food \( k \) to purchase, \( k = 1, \ldots, K \).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \times x_k
\]

\textbf{Subject to Nutritional Constraints:}
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \times x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M
\]

\textbf{Non-negativity Constraints:}
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\end{document}
```

This model captures the problem of selecting the optimal quantities of foods to minimize cost while satisfying nutritional requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model for Minimizing Food Costs}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_k \) denote the quantity of food \( k \) to purchase, \( k = 1, \ldots, K \).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \times x_k
\]

\textbf{Subject to Nutritional Constraints:}
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \times x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M
\]

\textbf{Non-negativity Constraints:}
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the input
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

#### Number of food items
K = len(data['price'])

#### Number of nutritional constraints
M = len(data['demand'])

#### Create the Linear Programming problem
problem = pulp.LpProblem("Minimize_Food_Costs", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total Cost"

#### Nutritional Constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f"Nutritional_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

