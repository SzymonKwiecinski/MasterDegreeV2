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
To formulate this problem, we need to set up a linear programming model where the objective is to maximize the profit from producing different spare parts, subject to the shop capacity constraints. Let's define the necessary variables and constraints.

######### Decision Variables
- \( x_k \): Quantity of spare part \( k \) to be produced, for \( k = 1, 2, \ldots, K \).

######### Parameters
- \( \text{time}_{k, s} \): Worker-hours required for part \( k \) in shop \( s \).
- \( \text{profit}_k \): Profit per unit of part \( k \).
- \( \text{capacity}_s \): Total available worker-hours in shop \( s \).

######### Objective Function
We want to maximize the total profit, given by:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

######### Constraints
- For each shop \( s \), the worker-hours used should not exceed the capacity:
\[
\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_s, \quad \text{for } s = 1, 2, \ldots, S
\]
- Non-negativity constraints: 
\[
x_k \geq 0, \quad \text{for } k = 1, 2, \ldots, K
\]

Now let's write this formulation in LaTeX code:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Spare Parts Production}

\subsection*{Objective}
Maximize the profit from producing spare parts:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Subject to Constraints}
\begin{align*}
\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k & \leq \text{capacity}_s, \quad \text{for } s = 1, 2, \ldots, S \\
x_k & \geq 0, \quad \text{for } k = 1, 2, \ldots, K
\end{align*}

\subsection*{Decision Variables}
- \( x_k \): Quantity of spare part \( k \) to be produced.

\subsection*{Parameters}
- \( \text{time}_{k, s} \): Worker-hours for part \( k \) in shop \( s \).
- \( \text{profit}_k \): Profit per unit of part \( k \).
- \( \text{capacity}_s \): Capacity of shop \( s \) in worker-hours.

\end{document}
```

Copy this LaTeX code into a `.tex` file or use a LaTeX editor to generate the document containing the linear programming model. This model will help you determine the optimal quantities of each spare part to produce in order to maximize overall profit while respecting shop capacities.

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

\subsection*{Objective}
Maximize the profit from producing spare parts:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Subject to Constraints}
\begin{align*}
\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k & \leq \text{capacity}_s, \quad \text{for } s = 1, 2, \ldots, S \\
x_k & \geq 0, \quad \text{for } k = 1, 2, \ldots, K
\end{align*}

\subsection*{Decision Variables}
- \( x_k \): Quantity of spare part \( k \) to be produced.

\subsection*{Parameters}
- \( \text{time}_{k, s} \): Worker-hours for part \( k \) in shop \( s \).
- \( \text{profit}_k \): Profit per unit of part \( k \).
- \( \text{capacity}_s \): Capacity of shop \( s \) in worker-hours.

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

#### Number of spare parts and shops
K = len(data['profit'])
S = len(data['capacity'])

#### Initialize the problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s], f"Capacity_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

