# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Food Selection Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $K$: Number of different types of food
    \item $M$: Number of nutrients to consider
    \item $Price_k$: Price of food $k$ for $k = 1, 2, \ldots, K$
    \item $Demand_m$: Demand for nutrient $m$ for $m = 1, 2, \ldots, M$
    \item $Nutrition_{k,m}$: Amount of nutrient $m$ in food $k$ for $k = 1, 2, \ldots, K$ and $m = 1, 2, \ldots, M$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Number of units purchased from food type $k$ for $k = 1, 2, \ldots, K$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of the foods purchased:
\[
\text{Minimize} \quad \sum_{k=1}^{K} Price_k \cdot x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item The total amount of each nutrient from all food types must meet or exceed the specific demand for that nutrient:
    \[
    \sum_{k=1}^{K} Nutrition_{k,m} \cdot x_k \geq Demand_m \quad \text{for } m = 1, 2, \ldots, M
    \]
    \item The number of units purchased from each food type is non-negative:
    \[
    x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5], 
        [1, 3], 
        [4, 4]
    ]
}

#### Number of food types (K) and nutrients (M)
K = len(data['price'])
M = len(data['demand'])

#### Problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K))

#### Constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

