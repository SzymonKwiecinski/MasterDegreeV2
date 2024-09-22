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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Nutritional Diet}

\textbf{Sets:}
\begin{itemize}
    \item Let $K$ be the set of foods, indexed by $k = 1, \ldots, K$.
    \item Let $M$ be the set of nutrients, indexed by $m = 1, \ldots, M$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $price_k$: price per unit of food $k$.
    \item $demand_m$: minimum required units of nutrient $m$ per day.
    \item $nutri_{k,m}$: units of nutrient $m$ contained in one unit of food $k$.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $quantity_k$: quantity of food $k$ to purchase.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{k=1}^{K} price_k \cdot quantity_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} nutri_{k,m} \cdot quantity_k \geq demand_m \quad \forall m \in M
\]

\textbf{Non-negativity Constraints:}
\[
quantity_k \geq 0 \quad \forall k \in K
\]

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

\section*{Linear Programming Model for Nutritional Diet}

\textbf{Sets:}
\begin{itemize}
    \item Let $K$ be the set of foods, indexed by $k = 1, \ldots, K$.
    \item Let $M$ be the set of nutrients, indexed by $m = 1, \ldots, M$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $price_k$: price per unit of food $k$.
    \item $demand_m$: minimum required units of nutrient $m$ per day.
    \item $nutri_{k,m}$: units of nutrient $m$ contained in one unit of food $k$.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $quantity_k$: quantity of food $k$ to purchase.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{k=1}^{K} price_k \cdot quantity_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} nutri_{k,m} \cdot quantity_k \geq demand_m \quad \forall m \in M
\]

\textbf{Non-negativity Constraints:}
\[
quantity_k \geq 0 \quad \forall k \in K
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data_json = '{"price": [1, 2, 3], "demand": [10, 20], "nutrition": [[3, 5], [1, 3], [4, 4]]}'
data = json.loads(data_json)

#### Extracting data from the JSON
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

#### Sets
K = range(len(price))  #### Foods
M = range(len(demand))  #### Nutrients

#### Creating the linear programming problem
problem = pulp.LpProblem("Nutritional_Diet_Problem", pulp.LpMinimize)

#### Variables
quantity = pulp.LpVariable.dicts("quantity", K, lowBound=0)

#### Objective Function
problem += pulp.lpSum(price[k] * quantity[k] for k in K), "Total Cost"

#### Constraints for nutrients
for m in M:
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in K) >= demand[m], f"Nutrient_Requirement_{m}"

#### Solving the problem
problem.solve()

#### Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

