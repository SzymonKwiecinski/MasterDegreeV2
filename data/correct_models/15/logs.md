# START: OR_ModelCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. You receive task description between <TASK_DESCRIPTION> and </TASK_DESCRIPTION>. You receive target objective between <OBJECTIVE> and </OBJECTIVE>. You receive description of constraints between <CONSTRAINTS> and </CONSTRAINTS>. You receive all 'parameters' which you have to use in model with symbol and shape between <PARAMETERS> and </PARAMETERS>. 
## START MESSAGE 0 
### ROLE: Role.USER
<TASK_DESCRIPTION>: A manufacturer needs to determine the optimal monthly production quantities for different types of parts, taking into account machine time constraints, machine costs, sales prices, and minimum production requirements.</TASK_DESCRIPTION>.
<OBJECTIVE>: Maximize the profit, which is the total sales minus the costs of using the machines </OBJECTIVE>
<CONSTRAINTS>
<CONSTRAINT>Number of batches for each part is non-negative</CONSTRAINT>
<CONSTRAINT>Total time used on each machine does not exceed its Availability</CONSTRAINT>
<CONSTRAINT>At least MinBatches of each part must be produced</CONSTRAINT>
</CONSTRAINTS>
<PARAMETERS>
<PARAMETER>
<DEFINITION>Number of parts</DEFINITION>
<SYMBOL>P</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Number of machines</DEFINITION>
<SYMBOL>M</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Time required to produce one batch of part p on machine m</DEFINITION>
<SYMBOL>TimeRequired</SYMBOL>
<SHAPE>['M', 'P']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Cost associated with using machine m</DEFINITION>
<SYMBOL>MachineCosts</SYMBOL>
<SHAPE>['M']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Availability of machine m per month</DEFINITION>
<SYMBOL>Availability</SYMBOL>
<SHAPE>['M']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Selling price of one batch of part p</DEFINITION>
<SYMBOL>Prices</SYMBOL>
<SHAPE>['P']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Minimum number of batches of part p to be produced</DEFINITION>
<SYMBOL>MinBatches</SYMBOL>
<SHAPE>['P']</SHAPE>
 </PARAMETER>
</PARAMETERS>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of parts
    \item $M$: Number of machines
    \item $TimeRequired_{m,p}$: Time required to produce one batch of part $p$ on machine $m$
    \item $MachineCosts_m$: Cost associated with using machine $m$
    \item $Availability_m$: Availability of machine $m$ per month
    \item $Prices_p$: Selling price of one batch of part $p$
    \item $MinBatches_p$: Minimum number of batches of part $p$ to be produced
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_p$: Number of batches of part $p$ to be produced
\end{itemize}

\subsection*{Objective Function}
Maximize the profit, which is the total sales minus the costs of using the machines:
\[
\text{Maximize } Z = \sum_{p=1}^{P} Prices_p \cdot x_p - \sum_{m=1}^{M} MachineCosts_m \cdot \sum_{p=1}^{P} TimeRequired_{m,p} \cdot x_p
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Non-negativity constraint for the number of batches:
    \[
    x_p \geq 0 \quad \forall p = 1, 2, \ldots, P
    \]
    \item Machine time availability constraint:
    \[
    \sum_{p=1}^{P} TimeRequired_{m,p} \cdot x_p \leq Availability_m \quad \forall m = 1, 2, \ldots, M
    \]
    \item Minimum production requirement:
    \[
    x_p \geq MinBatches_p \quad \forall p = 1, 2, \ldots, P
    \]
\end{enumerate}

\end{document}
```

# START: PythonProgrammerCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Print at the end the objective between <OBJ></OBJ> Do not include 'pip install' in script. Assume every python package is installed like in this example `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of parts
    \item $M$: Number of machines
    \item $TimeRequired_{m,p}$: Time required to produce one batch of part $p$ on machine $m$
    \item $MachineCosts_m$: Cost associated with using machine $m$
    \item $Availability_m$: Availability of machine $m$ per month
    \item $Prices_p$: Selling price of one batch of part $p$
    \item $MinBatches_p$: Minimum number of batches of part $p$ to be produced
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_p$: Number of batches of part $p$ to be produced
\end{itemize}

\subsection*{Objective Function}
Maximize the profit, which is the total sales minus the costs of using the machines:
\[
\text{Maximize } Z = \sum_{p=1}^{P} Prices_p \cdot x_p - \sum_{m=1}^{M} MachineCosts_m \cdot \sum_{p=1}^{P} TimeRequired_{m,p} \cdot x_p
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Non-negativity constraint for the number of batches:
    \[
    x_p \geq 0 \quad \forall p = 1, 2, \ldots, P
    \]
    \item Machine time availability constraint:
    \[
    \sum_{p=1}^{P} TimeRequired_{m,p} \cdot x_p \leq Availability_m \quad \forall m = 1, 2, \ldots, M
    \]
    \item Minimum production requirement:
    \[
    x_p \geq MinBatches_p \quad \forall p = 1, 2, \ldots, P
    \]
\end{enumerate}

\end{document}
```
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}
</DATA>

## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

#### Parameters
P = len(data['prices'])  #### Number of parts
M = len(data['machine_costs'])  #### Number of machines
TimeRequired = data['time_required']  #### Time required to produce one batch
MachineCosts = data['machine_costs']  #### Costs associated with using machines
Availability = data['availability']  #### Availability of machines
Prices = data['prices']  #### Selling prices of parts
MinBatches = data['min_batches']  #### Minimum number of batches to produce

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)  #### Number of batches for each part

#### Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Objective Function
profit = pulp.lpSum([Prices[p] * x[p] for p in range(P)]) - \
         pulp.lpSum([MachineCosts[m] * pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) for m in range(M)])

problem += profit

#### Constraints
#### Machine time availability constraints
for m in range(M):
    problem += pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) <= Availability[m]

#### Minimum production requirement constraints
for p in range(P):
    problem += x[p] >= MinBatches[p]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

