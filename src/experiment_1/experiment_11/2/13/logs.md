# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Optimal Production of Spare Parts}

\subsection*{Parameters}
\begin{itemize}
    \item $K$: Number of different spare parts
    \item $S$: Number of machines capable of making the spare parts
    \item $Time_{ks}$: Time taken to make spare part $k$ on machine $s$ for $k = 1, 2, \ldots, K$ and $s = 1, 2, \ldots, S$
    \item $Profit_k$: Profit obtained from making spare part $k$ for $k = 1, 2, \ldots, K$
    \item $Capacity_s$: Capacity of machine $s$ for the spare parts for $s = 1, 2, \ldots, S$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Quantity of spare part $k$ to produce for $k = 1, 2, \ldots, K$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit from producing the spare parts:
\[
\text{Maximize } Z = \sum_{k=1}^{K} Profit_k \cdot x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Quantities of each spare part must be non-negative:
    \[
    x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
    \]
    
    \item Time to produce each spare part must not exceed the available machine time:
    \[
    \sum_{k=1}^{K} Time_{ks} \cdot x_k \leq Capacity_s \quad \text{for } s = 1, 2, \ldots, S
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],  #### Time taken to make each spare part on each machine
    'profit': [30, 20, 40, 25, 10],  #### Profit associated with each spare part
    'capacity': [700, 1000]  #### Capacity of each machine
}

#### Parameters
K = len(data['profit'])  #### Number of spare parts
S = len(data['capacity'])  #### Number of machines

#### Create the linear programming problem
problem = pulp.LpProblem("Optimal_Production", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### Quantity of each spare part to produce

#### Objective function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s], f"Machine_Capacity_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

