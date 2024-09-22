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
To formulate the given problem as a linear programming (LP) problem, we will define a mathematical model. This model will focus on selecting quantities of different foods such that the total cost is minimized while meeting the nutritional demands.

**Set Definitions:**
- Let \( K \) be the number of different foods available.
- Let \( M \) be the number of different nutritional ingredients.

**Parameters:**
- \( \text{price}_k \): The cost per unit of food \( k \).
- \( \text{demand}_m \): The minimum daily units required for nutrient \( m \).
- \( \text{nutri}_{k,m} \): The units of nutrient \( m \) in one unit of food \( k \).

**Decision Variables:**
- \( \text{quantity}_k \): The number of units of food \( k \) to purchase.

**Objective:**
Minimize the total cost of purchasing foods:
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

**Constraints:**
Ensure that the nutritional requirements are met for each nutrient \( m \):
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \text{for all } m = 1, \ldots, M
\]

\(\text{quantity}_k \geq 0\) for all \( k = 1, \ldots, K\)

Now, we will represent the above model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Balanced Diet Problem}

\subsection*{Objective Function}
Minimize the total cost:
\[
Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
\begin{itemize}
    \item Nutritional requirements:
    \[
    \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \text{for all } m = 1, \ldots, M
    \]

    \item Non-negativity:
    \[
    \text{quantity}_k \geq 0 \quad \text{for all } k = 1, \ldots, K
    \]
\end{itemize}

\end{document}
```

This LaTeX document provides a complete representation of the linear programming model for the balanced diet problem. The objective is to minimize the cost, given the nutritional constraints and the non-negativity requirement for the quantities of food.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Balanced Diet Problem}

\subsection*{Objective Function}
Minimize the total cost:
\[
Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
\begin{itemize}
    \item Nutritional requirements:
    \[
    \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \text{for all } m = 1, \ldots, M
    \]

    \item Non-negativity:
    \[
    \text{quantity}_k \geq 0 \quad \text{for all } k = 1, \ldots, K
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

#### Parameters
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

#### Create problem
problem = pulp.LpProblem("Balanced_Diet_Problem", pulp.LpMinimize)

#### Decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(len(prices))]

#### Objective function
problem += pulp.lpSum(prices[k] * quantities[k] for k in range(len(prices)))

#### Constraints
#### Nutritional requirements
for m in range(len(demands)):
    problem += pulp.lpSum(nutrition[k][m] * quantities[k] for k in range(len(prices))) >= demands[m]

#### Solve the problem
problem.solve()

#### Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

