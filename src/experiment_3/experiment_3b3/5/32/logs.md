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

\subsection*{Variables}
Let \( x_k \) be the quantity produced of product \( k \) for \( k = 1, \ldots, K \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{produce\_time}_{k,s} \): Time required to produce 1 unit of product \( k \) in stage \( s \).
    \item \( \text{time}_s \): Available working hours for stage \( s \).
    \item \( \text{profit}_k \): Profit per unit of product \( k \).
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Constraints}
For each stage \( s \) (where \( s = 1, \ldots, S \)), the total production time must not exceed available time:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_s, \quad \forall s = 1, \ldots, S
\]

\subsection*{Non-negativity Constraints}
The production quantities must be non-negative:
\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\subsection*{Output Format}
The output quantity for each product \( k \):
\[
\text{quantity} = [x_1, x_2, \ldots, x_K]
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

\subsection*{Variables}
Let \( x_k \) be the quantity produced of product \( k \) for \( k = 1, \ldots, K \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{produce\_time}_{k,s} \): Time required to produce 1 unit of product \( k \) in stage \( s \).
    \item \( \text{time}_s \): Available working hours for stage \( s \).
    \item \( \text{profit}_k \): Profit per unit of product \( k \).
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Constraints}
For each stage \( s \) (where \( s = 1, \ldots, S \)), the total production time must not exceed available time:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_s, \quad \forall s = 1, \ldots, S
\]

\subsection*{Non-negativity Constraints}
The production quantities must be non-negative:
\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\subsection*{Output Format}
The output quantity for each product \( k \):
\[
\text{quantity} = [x_1, x_2, \ldots, x_K]
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Problem data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Number of products and machines
K = data['NumProducts']
S = data['NumMachines']

#### Production time and profit data
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K))

#### Constraints for each machine stage
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s]

#### Solve the problem
problem.solve()

#### Output the results
quantities = [pulp.value(x[k]) for k in range(K)]
print(f'Product Quantities: {quantities}')

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

