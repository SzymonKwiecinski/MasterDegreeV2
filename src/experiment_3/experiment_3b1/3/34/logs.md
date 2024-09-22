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
    \item Let \( M \) be the number of different nutritional ingredients.
    \item Let \( \text{price}_{k} \) be the price per unit of food \( k \).
    \item Let \( \text{demand}_{m} \) be the minimum requirement of nutrient \( m \) per day.
    \item Let \( \text{nutri}_{k, m} \) be the amount of nutrient \( m \) in food \( k \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_{k} \) be the quantity of food \( k \) to purchase.
\end{itemize}

\subsection*{Objective Function}
We aim to minimize the total cost of food purchased:
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_{k} \cdot x_{k}
\]

\subsection*{Constraints}
Each individual must receive at least the required amount of each nutrient:
\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_{k} \geq \text{demand}_{m}, \quad m = 1, \ldots, M
\]

\subsection*{Non-negativity Constraints}
\[
x_{k} \geq 0, \quad k = 1, \ldots, K
\]

\subsection*{Summary}
The complete linear programming model can be summarized as:
\[
\begin{align*}
\text{Minimize } & Z = \sum_{k=1}^{K} \text{price}_{k} \cdot x_{k} \\
\text{subject to } & \sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_{k} \geq \text{demand}_{m}, \quad m = 1, \ldots, M \\
& x_{k} \geq 0, \quad k = 1, \ldots, K
\end{align*}
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
    \item Let \( M \) be the number of different nutritional ingredients.
    \item Let \( \text{price}_{k} \) be the price per unit of food \( k \).
    \item Let \( \text{demand}_{m} \) be the minimum requirement of nutrient \( m \) per day.
    \item Let \( \text{nutri}_{k, m} \) be the amount of nutrient \( m \) in food \( k \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_{k} \) be the quantity of food \( k \) to purchase.
\end{itemize}

\subsection*{Objective Function}
We aim to minimize the total cost of food purchased:
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_{k} \cdot x_{k}
\]

\subsection*{Constraints}
Each individual must receive at least the required amount of each nutrient:
\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_{k} \geq \text{demand}_{m}, \quad m = 1, \ldots, M
\]

\subsection*{Non-negativity Constraints}
\[
x_{k} \geq 0, \quad k = 1, \ldots, K
\]

\subsection*{Summary}
The complete linear programming model can be summarized as:
\[
\begin{align*}
\text{Minimize } & Z = \sum_{k=1}^{K} \text{price}_{k} \cdot x_{k} \\
\text{subject to } & \sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_{k} \geq \text{demand}_{m}, \quad m = 1, \ldots, M \\
& x_{k} \geq 0, \quad k = 1, \ldots, K
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

#### Parameters
K = len(data['price'])  #### Number of different foods
M = len(data['demand'])  #### Number of different nutritional ingredients
prices = data['price']
demands = data['demand']
nutrients = data['nutrition']

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### Quantity of food k to purchase

#### Objective Function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints
for m in range(M):
    problem += pulp.lpSum(nutrients[k][m] * x[k] for k in range(K)) >= demands[m], f"Nutrient_Constraint_{m+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

