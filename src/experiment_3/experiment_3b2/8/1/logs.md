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
To solve this problem, we need to build a linear programming model that determines the optimal quantity of each good the firm should produce to maximize revenue, given the constraints on raw materials.

Let's define:
- \( x_j \) as the number of units of good \( j \) produced, for \( j = 1, \ldots, M \).

The objective is to maximize the total revenue:

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} \text{price}_j \cdot x_j
\]

Subject to raw material constraints:

For each raw material \( i = 1, \ldots, N \):

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i
\]

And non-negativity constraints:

\[
x_j \geq 0 \quad \text{for all } j = 1, \ldots, M
\]

Below is the complete linear programming model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Production Optimization}
\author{}
\date{}
\maketitle

\section*{Objective Function}
Maximize the total revenue:
\[
Z = \sum_{j=1}^{M} \text{price}_j \cdot x_j
\]

\section*{Constraints}
\begin{align*}
\text{For each raw material } i = 1, \ldots, N: \\
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j &\leq \text{available}_i
\end{align*}

\section*{Non-negativity Constraints}
\[
x_j \geq 0 \quad \text{for all } j = 1, \ldots, M
\]

\end{document}
```

This model will allow you to determine the optimal production quantities of each good to maximize the firm's revenue, while respecting the availability constraints of the raw materials. You can solve this linear programming problem using a solver like LINGO, Gurobi, or Python's SciPy `linprog` library.

