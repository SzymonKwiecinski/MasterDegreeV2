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
    \item Let \( K \) be the number of different foods available.
    \item Let \( M \) be the number of nutritional ingredients.
    \item Let \( \text{price}_k \) be the price per unit of food \( k \) for \( k = 1, \ldots, K \).
    \item Let \( \text{demand}_m \) be the minimum required units of nutrient \( m \) for \( m = 1, \ldots, M \).
    \item Let \( \text{nutri}_{k,m} \) be the units of nutrient \( m \) contained in food \( k \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( \text{quantity}_k \) be the quantity of food \( k \) to purchase for \( k = 1, \ldots, K \).
\end{itemize}

\subsection*{Objective Function}
We want to minimize the total price of the foods purchased:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
The following constraints must be satisfied to meet the nutritional demands:
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \text{for } m = 1, \ldots, M
\]

\subsection*{Non-negativity Constraints}
\[
\text{quantity}_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Summary}
The complete linear programming model can be stated as follows:
\begin{align*}
    \text{Minimize} & \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k \\
    \text{subject to} & \quad \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m, \quad m = 1, \ldots, M \\
    & \quad \text{quantity}_k \geq 0, \quad k = 1, \ldots, K 
\end{align*}

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
    \item Let \( K \) be the number of different foods available.
    \item Let \( M \) be the number of nutritional ingredients.
    \item Let \( \text{price}_k \) be the price per unit of food \( k \) for \( k = 1, \ldots, K \).
    \item Let \( \text{demand}_m \) be the minimum required units of nutrient \( m \) for \( m = 1, \ldots, M \).
    \item Let \( \text{nutri}_{k,m} \) be the units of nutrient \( m \) contained in food \( k \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( \text{quantity}_k \) be the quantity of food \( k \) to purchase for \( k = 1, \ldots, K \).
\end{itemize}

\subsection*{Objective Function}
We want to minimize the total price of the foods purchased:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
The following constraints must be satisfied to meet the nutritional demands:
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \text{for } m = 1, \ldots, M
\]

\subsection*{Non-negativity Constraints}
\[
\text{quantity}_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Summary}
The complete linear programming model can be stated as follows:
\begin{align*}
    \text{Minimize} & \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k \\
    \text{subject to} & \quad \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m, \quad m = 1, \ldots, M \\
    & \quad \text{quantity}_k \geq 0, \quad k = 1, \ldots, K 
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

#### Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

#### Prices, Nutritional values and Demands
prices = data['price']
nutrition = data['nutrition']
demands = data['demand']

#### Initialize the optimization problem
problem = pulp.LpProblem("Food_Optimization", pulp.LpMinimize)

#### Decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(prices[k] * quantities[k] for k in range(K)), "Total Cost"

#### Nutritional constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantities[k] for k in range(K)) >= demands[m], f"Nutrient_{m}_Demand"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

