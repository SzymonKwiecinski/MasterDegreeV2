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

\subsection*{Parameters}
\begin{itemize}
    \item Let \( K \) be the number of products.
    \item Let \( S \) be the number of stages.
    \item Let \( \text{produce\_time}_{k,s} \) be the time required to produce 1 unit of product \( k \) in stage \( s \) (in hours).
    \item Let \( \text{time}_s \) be the available working hours for stage \( s \).
    \item Let \( \text{profit}_k \) be the profit per unit of product \( k \).
\end{itemize}

\subsection*{Decision Variables}
Let \( x_k \) be the quantity produced of product \( k \).

\subsection*{Objective Function}
The objective is to maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Constraints}
The production must satisfy the time constraints for each stage:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_s \quad \forall s = 1, \ldots, S
\]

Additionally, the production quantities must be non-negative:
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\subsection*{Output}
The output will be:
\[
\text{quantity} = [x_k \text{ for } k = 1, \ldots, K]
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
    \item Let \( K \) be the number of products.
    \item Let \( S \) be the number of stages.
    \item Let \( \text{produce\_time}_{k,s} \) be the time required to produce 1 unit of product \( k \) in stage \( s \) (in hours).
    \item Let \( \text{time}_s \) be the available working hours for stage \( s \).
    \item Let \( \text{profit}_k \) be the profit per unit of product \( k \).
\end{itemize}

\subsection*{Decision Variables}
Let \( x_k \) be the quantity produced of product \( k \).

\subsection*{Objective Function}
The objective is to maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Constraints}
The production must satisfy the time constraints for each stage:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_s \quad \forall s = 1, \ldots, S
\]

Additionally, the production quantities must be non-negative:
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\subsection*{Output}
The output will be:
\[
\text{quantity} = [x_k \text{ for } k = 1, \ldots, K]
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data obtained from the JSON
data = {
    'NumProducts': 2, 
    'NumMachines': 2, 
    'ProduceTime': [[1, 3], [2, 1]], 
    'AvailableTime': [200, 100], 
    'Profit': [20, 10]
}

#### Number of products
K = data['NumProducts']
#### Number of stages
S = data['NumMachines']
#### Time required to produce one unit of each product at each stage
produce_time = data['ProduceTime']
#### Available time at each stage
available_time = data['AvailableTime']
#### Profit for each product
profit = data['Profit']

#### Create the problem variable to contain the problem data
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K))

#### Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s]

#### Solve the problem
problem.solve()

#### Print the results
quantity = [pulp.value(x[k]) for k in range(K)]
print("Quantity produced for each product:", quantity)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

