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
To address the problem of minimizing the cost of food while meeting nutritional requirements, we will develop a linear programming model. Below is the LaTeX code to represent this model. The model aims to minimize the total cost of foods purchased, subject to nutritional constraints that ensure the dietary needs are met.

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( k \): Index for foods, \( k = 1, 2, \ldots, K \)
    \item \( m \): Index for nutrients, \( m = 1, 2, \ldots, M \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{price}_k \): Price per unit of food \( k \)
    \item \( \text{demand}_m \): Minimum required units of nutrient \( m \)
    \item \( \text{nutri}_{k, m} \): Units of nutrient \( m \) per unit of food \( k \)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{quantity}_k \): Quantity of food \( k \) to purchase
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of purchasing the foods:

\[
\min \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
Ensure that the nutritional requirements are satisfied for each nutrient:

\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot \text{quantity}_k \geq \text{demand}_m, \quad \forall m = 1, 2, \ldots, M
\]

\subsection*{Non-negativity Constraints}
\[
\text{quantity}_k \geq 0, \quad \forall k = 1, 2, \ldots, K
\]

\end{document}
```

In this model:
- The objective function aims to minimize the total cost by summing up the product of food prices and their respective quantities.
- The constraints ensure that the sum of nutrients provided by the chosen quantities of foods meets or exceeds the required nutritional demand.
- Non-negativity constraints ensure that we do not purchase negative quantities of food. 

This formulation will help in determining the optimal purchase quantities for the cheapest diet that meets all nutritional needs.

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

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( k \): Index for foods, \( k = 1, 2, \ldots, K \)
    \item \( m \): Index for nutrients, \( m = 1, 2, \ldots, M \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{price}_k \): Price per unit of food \( k \)
    \item \( \text{demand}_m \): Minimum required units of nutrient \( m \)
    \item \( \text{nutri}_{k, m} \): Units of nutrient \( m \) per unit of food \( k \)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{quantity}_k \): Quantity of food \( k \) to purchase
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of purchasing the foods:

\[
\min \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
Ensure that the nutritional requirements are satisfied for each nutrient:

\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot \text{quantity}_k \geq \text{demand}_m, \quad \forall m = 1, 2, \ldots, M
\]

\subsection*{Non-negativity Constraints}
\[
\text{quantity}_k \geq 0, \quad \forall k = 1, 2, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
price = [1, 2, 3]
demand = [10, 20]
nutrition = [
    [3, 5],  #### nutrient units per unit of food 1
    [1, 3],  #### nutrient units per unit of food 2
    [4, 4]   #### nutrient units per unit of food 3
]

#### Number of foods and nutrients
K = len(price)
M = len(demand)

#### Defining the Linear Programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "Total Cost"

#### Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"Nutrient_{m}_Requirement"

#### Solve the problem
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

