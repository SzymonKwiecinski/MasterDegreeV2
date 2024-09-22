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

\textbf{Given:}
\begin{itemize}
    \item Let \( K \) be the number of products.
    \item Let \( S \) be the number of production stages.
    \item Let \( \text{produce\_time}_{k,s} \) be the time required to produce 1 unit of product \( k \) in stage \( s \).
    \item Let \( \text{time}_{s} \) be the available time in hours for stage \( s \).
    \item Let \( \text{profit}_{k} \) be the profit per unit of product \( k \).
\end{itemize}

\textbf{Decision Variables:}
Let \( x_k \) be the quantity produced of product \( k \).

\textbf{Objective Function:}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k
\]

\textbf{Constraints:}
For each stage \( s \), the total time spent on production should not exceed the available time:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_{s}, \quad \forall s \in \{1, 2, \ldots, S\}
\]

\textbf{Non-negativity Constraints:}
\[
x_k \geq 0, \quad \forall k \in \{1, 2, \ldots, K\}
\]

\textbf{Model Summary:}
\begin{align*}
\text{Maximize } & Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k \\
\text{subject to } & \sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_{s}, \quad \forall s \in \{1, 2, \ldots, S\} \\
& x_k \geq 0, \quad \forall k \in \{1, 2, \ldots, K\}
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

\section*{Linear Programming Model}

\textbf{Given:}
\begin{itemize}
    \item Let \( K \) be the number of products.
    \item Let \( S \) be the number of production stages.
    \item Let \( \text{produce\_time}_{k,s} \) be the time required to produce 1 unit of product \( k \) in stage \( s \).
    \item Let \( \text{time}_{s} \) be the available time in hours for stage \( s \).
    \item Let \( \text{profit}_{k} \) be the profit per unit of product \( k \).
\end{itemize}

\textbf{Decision Variables:}
Let \( x_k \) be the quantity produced of product \( k \).

\textbf{Objective Function:}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k
\]

\textbf{Constraints:}
For each stage \( s \), the total time spent on production should not exceed the available time:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_{s}, \quad \forall s \in \{1, 2, \ldots, S\}
\]

\textbf{Non-negativity Constraints:}
\[
x_k \geq 0, \quad \forall k \in \{1, 2, \ldots, K\}
\]

\textbf{Model Summary:}
\begin{align*}
\text{Maximize } & Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k \\
\text{subject to } & \sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_{s}, \quad \forall s \in \{1, 2, \ldots, S\} \\
& x_k \geq 0, \quad \forall k \in \{1, 2, \ldots, K\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extraction from the provided JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Number of products and machines
K = data['NumProducts']  #### Number of products
S = data['NumMachines']   #### Number of stages/machines

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables: quantity produced of each product
x = pulp.LpVariable.dicts("Produce", range(K), lowBound=0)

#### Objective function: Maximize total profit
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints for each stage
for s in range(S):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * x[k] for k in range(K)) <= data['AvailableTime'][s], f"Time_Constraint_Stage_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

