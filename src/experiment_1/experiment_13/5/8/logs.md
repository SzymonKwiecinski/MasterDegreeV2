# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Production Optimization}

\subsection*{Parameters}
\begin{itemize}
    \item $NumProducts$: Number of different products
    \item $NumMachines$: Number of different machines
    \item $ProduceTime_{k,m}$: Time to produce one unit of product $k$ on machine $m$, for $k = 1, \ldots, NumProducts$ and $m = 1, \ldots, NumMachines$
    \item $AvailableTime_m$: Total available time on machine $m$, for $m = 1, \ldots, NumMachines$
    \item $Profit_k$: Profit from producing one unit of product $k$, for $k = 1, \ldots, NumProducts$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Quantity of product $k$ to be produced, for $k = 1, \ldots, NumProducts$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{NumProducts} Profit_k \cdot x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Non-negativity constraints for each product:
    \[
    x_k \geq 0 \quad \text{for } k = 1, \ldots, NumProducts
    \]
    \item Production time constraints for each machine:
    \[
    \sum_{k=1}^{NumProducts} ProduceTime_{k,m} \cdot x_k \leq AvailableTime_m \quad \text{for } m = 1, \ldots, NumMachines
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],  #### Time to produce each product on each machine
    'AvailableTime': [200, 100],      #### Available time for each machine
    'Profit': [20, 10]                #### Profit for each product
}

#### Create a problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("Product", range(data['NumProducts']), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumProducts'])), "Total_Profit"

#### Constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][m] * x[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][m], f"Machine_{m+1}_Time"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

