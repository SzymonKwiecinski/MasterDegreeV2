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

\subsection*{Variables}
Let \( x_k \) be the quantity of food \( k \) purchased, where \( k = 1, \ldots, K \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{price}_k \): Price per unit of food \( k \)
    \item \( \text{demand}_m \): Minimum required units of nutrient \( m \) per day
    \item \( \text{nutri}_{k,m} \): Units of nutrient \( m \) provided by one unit of food \( k \)
\end{itemize}

\subsection*{Objective Function}
We want to minimize the total cost of the food purchased:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\subsection*{Constraints}
We need to ensure that the nutritional requirements are met for each nutrient \( m \):
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m, \quad \forall m = 1, \ldots, M
\]

\subsection*{Non-negativity Constraints}
The quantities of food purchased must be non-negative:
\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\subsection*{Output}
The output will be the vector of quantities to purchase:
\[
\text{quantity} = \left[ x_1, x_2, \ldots, x_K \right]
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

\subsection*{Variables}
Let \( x_k \) be the quantity of food \( k \) purchased, where \( k = 1, \ldots, K \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{price}_k \): Price per unit of food \( k \)
    \item \( \text{demand}_m \): Minimum required units of nutrient \( m \) per day
    \item \( \text{nutri}_{k,m} \): Units of nutrient \( m \) provided by one unit of food \( k \)
\end{itemize}

\subsection*{Objective Function}
We want to minimize the total cost of the food purchased:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\subsection*{Constraints}
We need to ensure that the nutritional requirements are met for each nutrient \( m \):
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m, \quad \forall m = 1, \ldots, M
\]

\subsection*{Non-negativity Constraints}
The quantities of food purchased must be non-negative:
\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\subsection*{Output}
The output will be the vector of quantities to purchase:
\[
\text{quantity} = \left[ x_1, x_2, \ldots, x_K \right]
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from <DATA>
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],  #### Food 1 provides per unit
        [1, 3],  #### Food 2 provides per unit
        [4, 4]   #### Food 3 provides per unit
    ]
}

#### Initialize the Linear Program
problem = pulp.LpProblem("Diet_Problem", pulp.LpMinimize)

#### Number of foods (K)
K = len(data['price'])

#### Number of nutrients (M)
M = len(data['demand'])

#### Decision variables: x_k >= 0 for all k
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function: Minimize total cost
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)])

#### Constraints: Ensure nutritional requirements are met
for m in range(M):
    problem += pulp.lpSum([data['nutrition'][k][m] * x[k] for k in range(K)]) >= data['demand'][m]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Output the quantities to purchase
quantities = [pulp.value(x_k) for x_k in x]
print("Quantities to purchase:", quantities)
```

