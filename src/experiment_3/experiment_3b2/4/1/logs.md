# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A firm produces \var{M} different goods using \var{N} different raw materials.
- The firm has \var{available_{i}} of raw material \var{i} available.
- Good \var{j} requires \var{req_{i,j}} units of material \var{i} per unit produced.
- Good \var{j} results in a revenue of \var{price_j} per unit produced.


INPUT FORMAT: 

{
    "available": [available_{i} for i in 1, ..., N]
    "requirements": [[req_{i,j} for i in 1, ..., N] for j in 1, ..., M],
    "prices": [price_{j} for j in 1, ..., M]
}

OBJECTIVE: How much of each good should the firm produce in order to maximize its total revenue?

OUTPUT INFO:

- the amount of each good produced \var{amount_{j}}.

OUTPUT FORMAT:

{
    "amount": [amount_{j} for j in 1, ..., M]
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model this problem, we'll create a linear programming model with the objective of maximizing the firm's total revenue, subject to the constraints imposed by the available raw materials. The decision variables in this problem are the amounts to produce for each good (\(x_j\)). The constraints are on the raw materials available.

Here's how the linear programming model can be formulated in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Given:}
\begin{itemize}
    \item \(N\) different raw materials.
    \item \(M\) different goods.
    \item \( \text{available}_i \) is the amount of raw material \(i\) available.
    \item \( \text{req}_{i,j} \) is the amount of material \(i\) required to produce one unit of good \(j\).
    \item \(\text{price}_j\) is the revenue per unit produced of good \(j\).
\end{itemize}

\textbf{Decision Variables:}
\[
x_j = \text{amount of good } j \text{ produced, where } j = 1, \ldots, M
\]

\textbf{Objective:}
Maximize the total revenue:
\[
\text{maximize } \sum_{j=1}^{M} \text{price}_j \cdot x_j
\]

\textbf{Constraints:}
\begin{align*}
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j & \leq \text{available}_i, & \text{for } i = 1, \ldots, N \\
x_j & \geq 0, & \text{for } j = 1, \ldots, M
\end{align*}

\textbf{Where:}
\begin{itemize}
    \item The first constraint ensures that the total usage of each raw material does not exceed its available amount.
    \item The non-negativity constraint ensures that production amounts are non-negative.
\end{itemize}

\end{document}
```

This LaTeX model provides a complete formulation for the linear programming problem described. It combines the objective function with constraints to ensure the optimal production strategy within the resource limitations.

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
    \item \(N\) different raw materials.
    \item \(M\) different goods.
    \item \( \text{available}_i \) is the amount of raw material \(i\) available.
    \item \( \text{req}_{i,j} \) is the amount of material \(i\) required to produce one unit of good \(j\).
    \item \(\text{price}_j\) is the revenue per unit produced of good \(j\).
\end{itemize}

\textbf{Decision Variables:}
\[
x_j = \text{amount of good } j \text{ produced, where } j = 1, \ldots, M
\]

\textbf{Objective:}
Maximize the total revenue:
\[
\text{maximize } \sum_{j=1}^{M} \text{price}_j \cdot x_j
\]

\textbf{Constraints:}
\begin{align*}
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j & \leq \text{available}_i, & \text{for } i = 1, \ldots, N \\
x_j & \geq 0, & \text{for } j = 1, \ldots, M
\end{align*}

\textbf{Where:}
\begin{itemize}
    \item The first constraint ensures that the total usage of each raw material does not exceed its available amount.
    \item The non-negativity constraint ensures that production amounts are non-negative.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Provided data
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Total_Revenue", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(data['M']), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['Prices'][j] * x[j] for j in range(data['M'])), "Total_Revenue"

#### Constraints
for i in range(data['N']):
    problem += (pulp.lpSum(data['Requirements'][j][i] * x[j] for j in range(data['M'])) <= data['Available'][i]), f"Raw_Material_Usage_{i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

