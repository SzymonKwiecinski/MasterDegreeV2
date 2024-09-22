# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A small firm specializes in making some types of spare automobile parts. 
- Each part is has to go through several shops 
- The required worker-hours for part \var{k} in shop \var{s} is \var{time_{k, s}}.
- The profit of part \var{k} is \var{profit_{k}}.
- The capacity of shop \var{s} is \var{capacity_{s}} working hours.

INPUT FORMAT:

{
	"time": [[time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"profit": [profit_{k} for k in 1,...,K],
	"capacity": [capacity_{s} for s in 1,...,S]
}


OBJECTIVE: Formulate the problem of determining the quantities of each spare part to be made during the month so as to maximize profit.

OUTPUT INFO:

- \var{quantity} represents the amount of each spare part to be made

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate the given problem as a Linear Programming (LP) model, we need to define the decision variables, objective function, and constraints based on the provided information.

######### Decision Variables:
- Let \( x_k \) be the quantity of spare part \( k \) to be produced.

######### Objective Function:
- We want to maximize the total profit, which is the sum of the profits from all parts produced. The objective function can be expressed as:
  \[
  \text{Maximize} \quad \sum_{k=1}^{K} \text{profit}_k \cdot x_k
  \]

######### Constraints:
1. **Shop Capacity Constraints:**
   - The total time spent on producing all parts in each shop cannot exceed the shop's capacity. For each shop \( s \), the constraint is:
     \[
     \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_s
     \]

2. **Non-Negativity Constraints:**
   - The quantity of each part produced should be non-negative:
     \[
     x_k \geq 0 \quad \forall k = 1, \ldots, K
     \]

######### Complete Linear Programming Model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Spare Parts Production}

\subsection*{Decision Variables}
\begin{align*}
x_k & : \text{quantity of spare part } k \text{ to be produced}
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize} \quad & \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\end{align*}

\subsection*{Subject to Constraints}
\begin{align*}
\text{For each shop } s: \\
& \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_s \quad (s = 1, \ldots, S)
\end{align*}

\begin{align*}
\text{Non-negativity constraints:} \\
& x_k \geq 0 \quad \forall k = 1, \ldots, K
\end{align*}

\end{document}
```

This LP model can be solved using any LP solver to determine the optimal quantities of each spare part to produce in order to maximize the firm's profits under the given constraints. The solution will provide the values for \( x_k \) (i.e., the "quantity" of each part) in the output format specified.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Spare Parts Production}

\subsection*{Decision Variables}
\begin{align*}
x_k & : \text{quantity of spare part } k \text{ to be produced}
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize} \quad & \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\end{align*}

\subsection*{Subject to Constraints}
\begin{align*}
\text{For each shop } s: \\
& \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_s \quad (s = 1, \ldots, S)
\end{align*}

\begin{align*}
\text{Non-negativity constraints:} \\
& x_k \geq 0 \quad \forall k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
    'profit': [30, 20, 40, 25, 10], 
    'capacity': [700, 1000]
}

time = data['time']
profit = data['profit']
capacity = data['capacity']

#### Number of spare parts (K) and number of shops (S)
K = len(profit)
S = len(capacity)

#### Problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_constraint_shop_{s+1}"

#### Solve
problem.solve()

#### Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

