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
To formulate the given problem as a linear programming model, let's define the decision variables and constraints:

######### Decision Variables:
- Let \( x_k \) be the quantity of food \( k \) to purchase, where \( k = 1, \ldots, K \).

######### Objective Function:
- We want to minimize the total cost of the foods purchased. The objective function is:
  \[
  \text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
  \]

######### Constraints:
- Nutritional requirements: For each nutrient \( m = 1, \ldots, M \), the total nutrients provided by the foods must be at least the required demand:
  \[
  \sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M
  \]

- Non-negativity: The quantities of each food must be non-negative:
  \[
  x_k \geq 0 \quad \forall k = 1, \ldots, K
  \]

Below is the corresponding LaTeX code for this linear programming formulation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_k \): Quantity of food \( k \) to purchase, for \( k = 1, \ldots, K \).
\end{itemize}

\subsection*{Objective Function}
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\subsection*{Constraints}
\begin{itemize}
    \item Nutritional requirements for each nutrient \( m = 1, \ldots, M \):
    \[
    \sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M
    \]
    \item Non-negativity:
    \[
    x_k \geq 0 \quad \forall k = 1, \ldots, K
    \]
\end{itemize}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_k \): Quantity of food \( k \) to purchase, for \( k = 1, \ldots, K \).
\end{itemize}

\subsection*{Objective Function}
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\subsection*{Constraints}
\begin{itemize}
    \item Nutritional requirements for each nutrient \( m = 1, \ldots, M \):
    \[
    \sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M
    \]
    \item Non-negativity:
    \[
    x_k \geq 0 \quad \forall k = 1, \ldots, K
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

#### Extract data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

#### Number of food items and nutrients
K = len(price)
M = len(demand)

#### Create the problem
problem = pulp.LpProblem("Food_Optimization", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demand[m], f"Nutritional_Demand_{m+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

