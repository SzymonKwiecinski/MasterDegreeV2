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

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( K \) be the number of different foods.
    \item Let \( M \) be the number of nutritional ingredients.
    \item Let \( price_k \) be the price per unit of food \( k \) where \( k = 1, 2, \ldots, K \).
    \item Let \( demand_m \) be the minimum required units of nutrient \( m \) where \( m = 1, 2, \ldots, M \).
    \item Let \( nutri_{k, m} \) be the units of nutrient \( m \) contained in one unit of food \( k \).
\end{itemize}

\subsection*{Decision Variables}
Let \( quantity_k \) be the quantity of food \( k \) to purchase, where \( k = 1, 2, \ldots, K \).

\subsection*{Objective Function}
The objective is to minimize the total cost of the foods purchased:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} price_k \cdot quantity_k
\]

\subsection*{Constraints}
The nutritional constraints are defined by the requirements for each nutrient \( m \):
\[
\sum_{k=1}^{K} nutri_{k, m} \cdot quantity_k \geq demand_m \quad \forall m = 1, 2, \ldots, M
\]

\subsection*{Non-negativity Constraints}
The quantities of food purchased must be non-negative:
\[
quantity_k \geq 0 \quad \forall k = 1, 2, \ldots, K
\]

\subsection*{Output Format}
The result will include the quantities of each food to purchase:
\[
\{ "quantity": [quantity_k \text{ for } k = 1, \ldots, K] \}
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

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( K \) be the number of different foods.
    \item Let \( M \) be the number of nutritional ingredients.
    \item Let \( price_k \) be the price per unit of food \( k \) where \( k = 1, 2, \ldots, K \).
    \item Let \( demand_m \) be the minimum required units of nutrient \( m \) where \( m = 1, 2, \ldots, M \).
    \item Let \( nutri_{k, m} \) be the units of nutrient \( m \) contained in one unit of food \( k \).
\end{itemize}

\subsection*{Decision Variables}
Let \( quantity_k \) be the quantity of food \( k \) to purchase, where \( k = 1, 2, \ldots, K \).

\subsection*{Objective Function}
The objective is to minimize the total cost of the foods purchased:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} price_k \cdot quantity_k
\]

\subsection*{Constraints}
The nutritional constraints are defined by the requirements for each nutrient \( m \):
\[
\sum_{k=1}^{K} nutri_{k, m} \cdot quantity_k \geq demand_m \quad \forall m = 1, 2, \ldots, M
\]

\subsection*{Non-negativity Constraints}
The quantities of food purchased must be non-negative:
\[
quantity_k \geq 0 \quad \forall k = 1, 2, \ldots, K
\]

\subsection*{Output Format}
The result will include the quantities of each food to purchase:
\[
\{ "quantity": [quantity_k \text{ for } k = 1, \ldots, K] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extracting data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],
        [1, 3],
        [4, 4]
    ]
}

#### Parameters
K = len(data['price'])  #### Number of different foods
M = len(data['demand'])  #### Number of nutritional ingredients

#### Create the linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision Variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(data['price'][k] * quantities[k] for k in range(K)), "Total Cost"

#### Constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantities[k] for k in range(K)) >= data['demand'][m], f"Nutrition_{m}"

#### Solve the problem
problem.solve()

#### Prepare the output
result_quantities = [pulp.value(quantities[k]) for k in range(K)]

#### Display results
print({"quantity": result_quantities})
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

