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

\section*{Linear Programming Model for Production Optimization}

\subsection*{Definitions}
\begin{itemize}
    \item Let \( K \) be the number of products.
    \item Let \( S \) be the number of stages in production.
    \item Let \( \text{produce\_time}_{k,s} \) be the time required to produce 1 unit of product \( k \) at stage \( s \).
    \item Let \( \text{time}_{s} \) be the total available working hours for stage \( s \).
    \item Let \( \text{profit}_{k} \) be the profit earned from producing 1 unit of product \( k \).
    \item Let \( \text{quantity}_{k} \) be the quantity of product \( k \) to produce.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total profit:

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
The production must respect the available time for each stage. For each stage \( s \):

\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot \text{quantity}_{k} \leq \text{time}_{s} \quad \forall s = 1, \ldots, S
\]

\subsection*{Non-negativity Constraints}
The quantity produced for each product must be non-negative:

\[
\text{quantity}_{k} \geq 0 \quad \forall k = 1, \ldots, K
\]

\subsection*{Summary of the LP Model}
The complete linear programming model can be summarized as follows:

\begin{align*}
    \text{Maximize} \quad & Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k} \\
    \text{subject to} \quad & \sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot \text{quantity}_{k} \leq \text{time}_{s}, \quad \forall s = 1, \ldots, S \\
    & \text{quantity}_{k} \geq 0, \quad \forall k = 1, \ldots, K
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

\section*{Linear Programming Model for Production Optimization}

\subsection*{Definitions}
\begin{itemize}
    \item Let \( K \) be the number of products.
    \item Let \( S \) be the number of stages in production.
    \item Let \( \text{produce\_time}_{k,s} \) be the time required to produce 1 unit of product \( k \) at stage \( s \).
    \item Let \( \text{time}_{s} \) be the total available working hours for stage \( s \).
    \item Let \( \text{profit}_{k} \) be the profit earned from producing 1 unit of product \( k \).
    \item Let \( \text{quantity}_{k} \) be the quantity of product \( k \) to produce.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total profit:

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
The production must respect the available time for each stage. For each stage \( s \):

\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot \text{quantity}_{k} \leq \text{time}_{s} \quad \forall s = 1, \ldots, S
\]

\subsection*{Non-negativity Constraints}
The quantity produced for each product must be non-negative:

\[
\text{quantity}_{k} \geq 0 \quad \forall k = 1, \ldots, K
\]

\subsection*{Summary of the LP Model}
The complete linear programming model can be summarized as follows:

\begin{align*}
    \text{Maximize} \quad & Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k} \\
    \text{subject to} \quad & \sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot \text{quantity}_{k} \leq \text{time}_{s}, \quad \forall s = 1, \ldots, S \\
    & \text{quantity}_{k} \geq 0, \quad \forall k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Unpacking data
K = data['NumProducts']  #### Number of products
S = data['NumMachines']  #### Number of stages
produce_time = data['ProduceTime']
time_available = data['AvailableTime']
profit = data['Profit']

#### Create the problem instance
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K))

#### Constraints
for s in range(S):
    problem += (pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= time_available[s])

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

