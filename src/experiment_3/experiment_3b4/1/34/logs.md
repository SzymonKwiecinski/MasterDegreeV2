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
To solve this linear programming problem, we need to formulate the objective function and constraints based on the given data. The goal is to minimize the total cost of purchasing foods while satisfying the nutritional requirements. Let's outline the linear programming model:

######### Objective
Minimize the total cost of purchasing food items. We have:
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

######### Constraints
1. Nutritional constraints for each nutrient \( m \):
   \[
   \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \text{for each } m = 1, \ldots, M
   \]

2. Non-negativity constraints for each food \( k \):
   \[
   \text{quantity}_k \geq 0 \quad \text{for each } k = 1, \ldots, K
   \]

######### Model in LaTeX
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective}
Minimize the total cost of purchasing food items:
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
\begin{itemize}
    \item Nutritional constraints for each nutrient \( m \):
    \[
    \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \text{for each } m = 1, \ldots, M
    \]

    \item Non-negativity constraints:
    \[
    \text{quantity}_k \geq 0 \quad \text{for each } k = 1, \ldots, K
    \]
\end{itemize}

\end{document}
```

This model represents the problem in mathematical terms, where `quantity_k` denotes the amount of food \( k \) to purchase. The constraints ensure that the nutritional needs are met for each nutrient, and that the quantities of food are non-negative.

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

\subsection*{Objective}
Minimize the total cost of purchasing food items:
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
\begin{itemize}
    \item Nutritional constraints for each nutrient \( m \):
    \[
    \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \text{for each } m = 1, \ldots, M
    \]

    \item Non-negativity constraints:
    \[
    \text{quantity}_k \geq 0 \quad \text{for each } k = 1, \ldots, K
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

#### Parameters
prices = data['price']
demands = data['demand']
nutritional_values = data['nutrition']

#### Number of food items and nutrients
K = len(prices)
M = len(demands)

#### Problem
problem = pulp.LpProblem("Food_Purchase_Problem", pulp.LpMinimize)

#### Decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum(prices[k] * quantities[k] for k in range(K)), "Total_Cost"

#### Nutritional constraints
for m in range(M):
    problem += (pulp.lpSum(nutritional_values[k][m] * quantities[k] for k in range(K)) >= demands[m], f"Nutrient_{m}")

#### Solve problem
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

