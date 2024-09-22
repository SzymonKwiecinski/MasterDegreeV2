# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A company produces \var{S} different types of steel using \var{A} different alloys.
- The company has \var{available_{a}} tons of alloy \var{a} available.
- Steel \var{s} requires a certain percentage of carbon \var{carbon_min_{s}}.
- Steel \var{s} has a maximum allowable percentage for nickel \var{nickel_max_{s}}.
- Alloy \var{a} contains \var{carbon_{a}} percent of carbon and \var{nickel_{a}} percent of nickel.
- Alloy \var{a} has a purchase price of \var{alloy_price_{a}} per ton.
- Steel \var{s} has a selling price of \var{steel_price_{s}} per ton.
- All steel must have at most 40% of alloy 1.

INPUT FORMAT: 

{
"available": [available_{a} for a in 1, ..., A],
"carbon": [carbon_{a} for a in 1, ..., A],
"nickel": [nickel_{a} for a in 1, ..., A],
"alloy_prices": [alloy_price_{a} for a in 1, ..., A],
"steel_prices": [steel_price_{s} for s in 1, ..., S],
"carbon_min": [carbon_min_{s} for s in 1, ..., S],
"nickel_max": [nickel_min_{s} for s in 1, ..., S]
}

OBJECTIVE: How much of each alloy should the company use in each type of steel, and how much of each steel type should be produced to maximize profit?

OUTPUT INFO:

- The amount of each alloy used in each type of steel \var{alloy_amount_{a,s}}.
- \var{total_steel_{s}} shows the total amount of steel type \var{s} produced.
- \var{total_profit} represents the total profit.

OUTPUT FORMAT:

{
    "alloy_use": [[alloy_amount_{a,s} for a in 1, ..., A] for s in 1, ..., S],
    "total_steel": [total_steel_{s} for s in 1, ..., S],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Indices}
\begin{itemize}
    \item $s \in \{1, \ldots, S\}$: index for steel types
    \item $a \in \{1, \ldots, A\}$: index for alloys
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $available_{a}$: available tons of alloy $a$
    \item $carbon_{a}$: percentage of carbon in alloy $a$
    \item $nickel_{a}$: percentage of nickel in alloy $a$
    \item $alloy\_price_{a}$: purchase price of alloy $a$ per ton
    \item $steel\_price_{s}$: selling price of steel type $s$ per ton
    \item $carbon\_min_{s}$: minimum carbon percentage required for steel type $s$
    \item $nickel\_max_{s}$: maximum nickel percentage allowed for steel type $s$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $alloy\_amount_{a,s}$: amount of alloy $a$ used in steel type $s$
    \item $total\_steel_{s}$: total amount of steel type $s$ produced
    \item $total\_profit$: total profit from producing steel
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize } total\_profit = \sum_{s=1}^{S} (steel\_price_{s} \cdot total\_steel_{s}) - \sum_{a=1}^{A} (alloy\_price_{a} \cdot \sum_{s=1}^{S} alloy\_amount_{a,s})
\]

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Alloy Availability:}
    \[
    \sum_{s=1}^{S} alloy\_amount_{a,s} \leq available_{a}, \quad \forall a
    \]
    
    \item \textbf{Steel Production:}
    \[
    total\_steel_{s} = \sum_{a=1}^{A} alloy\_amount_{a,s}, \quad \forall s
    \]
    
    \item \textbf{Carbon Content:}
    \[
    \frac{\sum_{a=1}^{A} (carbon_{a} \cdot alloy\_amount_{a,s})}{total\_steel_{s}} \geq carbon\_min_{s}, \quad \forall s
    \]
    
    \item \textbf{Nickel Content:}
    \[
    \frac{\sum_{a=1}^{A} (nickel_{a} \cdot alloy\_amount_{a,s})}{total\_steel_{s}} \leq nickel\_max_{s}, \quad \forall s
    \]
    
    \item \textbf{Alloy 1 Constraint:}
    \[
    \sum_{s=1}^{S} alloy\_amount_{1,s} \leq 0.4 \cdot \sum_{s=1}^{S} total\_steel_{s}
    \]
    
    \item \textbf{Non-negativity:}
    \[
    alloy\_amount_{a,s} \geq 0, \quad \forall a, s
    \]
    \[
    total\_steel_{s} \geq 0, \quad \forall s
    \]
\end{itemize}

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

\subsection*{Indices}
\begin{itemize}
    \item $s \in \{1, \ldots, S\}$: index for steel types
    \item $a \in \{1, \ldots, A\}$: index for alloys
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $available_{a}$: available tons of alloy $a$
    \item $carbon_{a}$: percentage of carbon in alloy $a$
    \item $nickel_{a}$: percentage of nickel in alloy $a$
    \item $alloy\_price_{a}$: purchase price of alloy $a$ per ton
    \item $steel\_price_{s}$: selling price of steel type $s$ per ton
    \item $carbon\_min_{s}$: minimum carbon percentage required for steel type $s$
    \item $nickel\_max_{s}$: maximum nickel percentage allowed for steel type $s$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $alloy\_amount_{a,s}$: amount of alloy $a$ used in steel type $s$
    \item $total\_steel_{s}$: total amount of steel type $s$ produced
    \item $total\_profit$: total profit from producing steel
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize } total\_profit = \sum_{s=1}^{S} (steel\_price_{s} \cdot total\_steel_{s}) - \sum_{a=1}^{A} (alloy\_price_{a} \cdot \sum_{s=1}^{S} alloy\_amount_{a,s})
\]

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Alloy Availability:}
    \[
    \sum_{s=1}^{S} alloy\_amount_{a,s} \leq available_{a}, \quad \forall a
    \]
    
    \item \textbf{Steel Production:}
    \[
    total\_steel_{s} = \sum_{a=1}^{A} alloy\_amount_{a,s}, \quad \forall s
    \]
    
    \item \textbf{Carbon Content:}
    \[
    \frac{\sum_{a=1}^{A} (carbon_{a} \cdot alloy\_amount_{a,s})}{total\_steel_{s}} \geq carbon\_min_{s}, \quad \forall s
    \]
    
    \item \textbf{Nickel Content:}
    \[
    \frac{\sum_{a=1}^{A} (nickel_{a} \cdot alloy\_amount_{a,s})}{total\_steel_{s}} \leq nickel\_max_{s}, \quad \forall s
    \]
    
    \item \textbf{Alloy 1 Constraint:}
    \[
    \sum_{s=1}^{S} alloy\_amount_{1,s} \leq 0.4 \cdot \sum_{s=1}^{S} total\_steel_{s}
    \]
    
    \item \textbf{Non-negativity:}
    \[
    alloy\_amount_{a,s} \geq 0, \quad \forall a, s
    \]
    \[
    total\_steel_{s} \geq 0, \quad \forall s
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

#### Parameters
A = len(data['available'])  #### Number of alloys
S = len(data['steel_prices'])  #### Number of steel types

#### Create the problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

#### Objective Function
profit = pulp.lpSum([data['steel_prices'][s] * total_steel[s] for s in range(S)]) - \
         pulp.lpSum([data['alloy_prices'][a] * pulp.lpSum([alloy_amount[a][s] for s in range(S)]) for a in range(A)])
problem += profit

#### Constraints
#### Alloy Availability
for a in range(A):
    problem += pulp.lpSum([alloy_amount[a][s] for s in range(S)]) <= data['available'][a]

#### Steel Production
for s in range(S):
    problem += total_steel[s] == pulp.lpSum([alloy_amount[a][s] for a in range(A)])

#### Carbon Content
for s in range(S):
    problem += (pulp.lpSum([data['carbon'][a] * alloy_amount[a][s] for a in range(A)]) / total_steel[s]) >= data['carbon_min'][s]

#### Nickel Content
for s in range(S):
    problem += (pulp.lpSum([data['nickel'][a] * alloy_amount[a][s] for a in range(A)]) / total_steel[s]) <= data['nickel_max'][s]

#### Alloy 1 Constraint
problem += pulp.lpSum([alloy_amount[0][s] for s in range(S)]) <= \
           0.4 * pulp.lpSum([total_steel[s] for s in range(S)])

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

