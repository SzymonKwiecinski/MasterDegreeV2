# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We assume that there are available at the market different foods and that the food \var{k} sells at a price \var{price_{k}} per unit. 
- In addition there are several basic nutritional ingredients and, to achieve a balanced diet, each individual must receive at least \var{demand_{m}} units of nutrient \var{m} per day. 
- Finally, we assume that each unit of food \var{k} contains \var{nutri_{k, m}} units of nutrition \var{m}

INPUT FORMAT:

{
	"price": [price_{k} for k in 1,...,K],
	"demand": [demand_{m} for m in 1,...,M],
	"nutrition": [[nutri_{k, m} for m in 1,...,M] for k in 1,...,K]
}


OBJECTIVE: We want to minimize the total prices of the foods to purchase.

OUTPUT INFO:

- \var{quantity} represents the quantity of each food to purchase

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate the Linear Programming problem for the given scenario, the objective is to minimize the total cost of purchasing foods while satisfying the nutritional requirements. Below is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Diet Optimization Problem}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

\textbf{Given:}
\begin{itemize}
    \item Let \( K \) be the number of different foods.
    \item Let \( M \) be the number of different nutritional requirements.
    \item \( \text{price}_k \) is the price per unit of food \( k \) for \( k = 1, 2, \ldots, K \).
    \item \( \text{demand}_m \) is the demand of nutrient \( m \) for \( m = 1, 2, \ldots, M \).
    \item \( \text{nutri}_{k,m} \) is the amount of nutrient \( m \) contained in one unit of food \( k \).
\end{itemize}

\textbf{Objective:}
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \text{for each } m = 1, 2, \ldots, M
\]
\[
\text{quantity}_k \geq 0 \quad \text{for each } k = 1, 2, \ldots, K
\]

\textbf{Decision Variables:}
\begin{itemize}
    \item \( \text{quantity}_k \) represents the quantity of food \( k \) to purchase.
\end{itemize}

\end{document}
```

This model captures the essence of the diet problem, where the goal is to ensure that the nutritional demands are met at the minimum cost by selecting appropriate quantities of each type of food available.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Diet Optimization Problem}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

\textbf{Given:}
\begin{itemize}
    \item Let \( K \) be the number of different foods.
    \item Let \( M \) be the number of different nutritional requirements.
    \item \( \text{price}_k \) is the price per unit of food \( k \) for \( k = 1, 2, \ldots, K \).
    \item \( \text{demand}_m \) is the demand of nutrient \( m \) for \( m = 1, 2, \ldots, M \).
    \item \( \text{nutri}_{k,m} \) is the amount of nutrient \( m \) contained in one unit of food \( k \).
\end{itemize}

\textbf{Objective:}
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \text{for each } m = 1, 2, \ldots, M
\]
\[
\text{quantity}_k \geq 0 \quad \text{for each } k = 1, 2, \ldots, K
\]

\textbf{Decision Variables:}
\begin{itemize}
    \item \( \text{quantity}_k \) represents the quantity of food \( k \) to purchase.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

#### Number of different foods (K) and nutritional requirements (M)
K = len(data['price'])
M = len(data['demand'])

#### Create the linear programming problem
problem = pulp.LpProblem("Diet_Optimization", pulp.LpMinimize)

#### Decision variables: quantity of each food
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

#### Objective function: Minimize total cost
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K)), "Total_Cost"

#### Constraints: Nutritional requirements
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m], f"Nutritional_Requirement_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

