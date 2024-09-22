# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We suppose that some products can be produced, each of them passing through several stages.
- Necessary time to produce 1 unit of product \var{k} is \var{produce_time_{k, s}} hours for stage \var{s}.
- Availability in working hours is \var{time_{s}} for stage \var{s}. 
- The unitary profits for product \var{k} is \var{profit_{k}}.

INPUT FORMAT:

{
	"produce_time": [[produce_time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"available_time": [time_{s} for s in 1,...,S],
	"profit": [profit_{k} for k in 1,...,K]
}


OBJECTIVE: Determine the quantities to be produced such that all the production constraints are satisfied and the profit is maximized.

OUTPUT INFO:

- \var{quantity} represents the production quantity for each product

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

\subsection*{Sets}
Let:
\begin{itemize}
    \item \( K \) be the set of products, where \( k = 1, 2, \ldots, K \).
    \item \( S \) be the set of stages, where \( s = 1, 2, \ldots, S \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{produce\_time}_{k,s} \): Time required to produce 1 unit of product \( k \) at stage \( s \) (in hours).
    \item \( \text{time}_s \): Available time at stage \( s \) (in hours).
    \item \( \text{profit}_k \): Profit from producing 1 unit of product \( k \).
\end{itemize}

\subsection*{Decision Variables}
Let:
\[
\text{quantity}_k \quad \text{for } k = 1, 2, \ldots, K
\]
be the quantity of product \( k \) to be produced.

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
For each stage \( s \):
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot \text{quantity}_k \leq \text{time}_s \quad \text{for } s = 1, 2, \ldots, S
\]

\subsection*{Non-negativity Constraints}
\[
\text{quantity}_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
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

\subsection*{Sets}
Let:
\begin{itemize}
    \item \( K \) be the set of products, where \( k = 1, 2, \ldots, K \).
    \item \( S \) be the set of stages, where \( s = 1, 2, \ldots, S \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{produce\_time}_{k,s} \): Time required to produce 1 unit of product \( k \) at stage \( s \) (in hours).
    \item \( \text{time}_s \): Available time at stage \( s \) (in hours).
    \item \( \text{profit}_k \): Profit from producing 1 unit of product \( k \).
\end{itemize}

\subsection*{Decision Variables}
Let:
\[
\text{quantity}_k \quad \text{for } k = 1, 2, \ldots, K
\]
be the quantity of product \( k \) to be produced.

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}
For each stage \( s \):
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot \text{quantity}_k \leq \text{time}_s \quad \text{for } s = 1, 2, \ldots, S
\]

\subsection*{Non-negativity Constraints}
\[
\text{quantity}_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
\]

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
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Sets
K = range(data['NumProducts'])  #### Products
S = range(data['NumMachines'])   #### Stages

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
quantity = pulp.LpVariable.dicts("quantity", K, lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in K), "Total_Profit"

#### Constraints
for s in S:
    problem += pulp.lpSum(data['ProduceTime'][k][s] * quantity[k] for k in K) <= data['AvailableTime'][s], f"Time_Constraint_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

