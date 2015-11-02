#!/usr/bin/env python

#> \file
#> \author Chris Bradley
#> \brief This is an example script to solve a Laplace problem using OpenCMISS calls in python.
#>
#> \section LICENSE
#>
#> Version: MPL 1.1/GPL 2.0/LGPL 2.1
#>
#> The contents of this file are subject to the Mozilla Public License
#> Version 1.1 (the "License"); you may not use this file except in
#> compliance with the License. You may obtain a copy of the License at
#> http://www.mozilla.org/MPL/
#>
#> Software distributed under the License is distributed on an "AS IS"
#> basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
#> License for the specific language governing rights and limitations
#> under the License.
#>
#> The Original Code is OpenCMISS
#>
#> The Initial Developer of the Original Code is University of Auckland,
#> Auckland, New Zealand and University of Oxford, Oxford, United
#> Kingdom. Portions created by the University of Auckland and University
#> of Oxford are Copyright (C) 2007 by the University of Auckland and
#> the University of Oxford. All Rights Reserved.
#>
#> Contributor(s): Adam Reeve
#>
#> Alternatively, the contents of this file may be used under the terms of
#> either the GNU General Public License Version 2 or later (the "GPL"), or
#> the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
#> in which case the provisions of the GPL or the LGPL are applicable instead
#> of those above. if you wish to allow use of your version of this file only
#> under the terms of either the GPL or the LGPL, and not to allow others to
#> use your version of this file under the terms of the MPL, indicate your
#> decision by deleting the provisions above and replace them with the notice
#> and other provisions required by the GPL or the LGPL. if you do not delete
#> the provisions above, a recipient may use your version of this file under
#> the terms of any one of the MPL, the GPL or the LGPL.

# Add Python bindings directory to PATH
import sys, os
sys.path.append(os.sep.join((os.environ['OPENCMISS_ROOT'],'cm','bindings','python')))

# Intialise OpenCMISS start
from opencmiss import iron
# Intialise OpenCMISS end

iron.DiagnosticsSetOn(iron.DiagnosticTypes.IN,[1,2,3,4,5],"Diagnostics",["DOMAIN_MAPPINGS_LOCAL_FROM_GLOBAL_CALCULATE"])

# Get the computational nodes information
#DOC-START computationalNode
numberOfComputationalNodes = iron.ComputationalNumberOfNodesGet()
computationalNodeNumber = iron.ComputationalNodeNumberGet()
#DOC-END computationalNode

# Creation a RC coordinate system
#DOC-START coordinate1
coordinateSystem = iron.CoordinateSystem()
#DOC-END coordinate1
#DOC-START coordinate2
coordinateSystemUserNumber = 1
coordinateSystem.CreateStart(coordinateSystemUserNumber)
#DOC-END coordinate2
#DOC-START coordinate3
coordinateSystem.dimension = 3
#DOC-END coordinate3
#DOC-START coordinate4
coordinateSystem.CreateFinish()
#DOC-END coordinate4

# Create a region
#DOC-START region
regionUserNumber = 1
region = iron.Region()
region.CreateStart(regionUserNumber,iron.WorldRegion)
region.label = "LaplaceRegion"
region.coordinateSystem = coordinateSystem
region.CreateFinish()
#DOC-END region

# Create a tri-linear lagrange basis
#DOC-START basis
basisUserNumber = 1
basis = iron.Basis()
basis.CreateStart(basisUserNumber)
basis.type = iron.BasisTypes.LAGRANGE_HERMITE_TP
basis.numberOfXi = 3
basis.interpolationXi = [iron.BasisInterpolationSpecifications.LINEAR_LAGRANGE]*3
basis.quadratureNumberOfGaussXi = [2]*3
basis.CreateFinish()
#DOC-END basis

# Create a generated mesh
#DOC-START generated mesh
height = 1.0
width  = 2.0
length = 3.0
numberGlobalXElements = 5
numberGlobalYElements = 5
numberGlobalZElements = 5

meshComponentNumber = 1
generatedMeshUserNumber = 1
generatedMesh = iron.GeneratedMesh()
generatedMesh.CreateStart(generatedMeshUserNumber,region)
generatedMesh.type = iron.GeneratedMeshTypes.REGULAR
generatedMesh.basis = [basis]
generatedMesh.extent = [width,height,length]
generatedMesh.numberOfElements = [numberGlobalXElements,numberGlobalYElements,numberGlobalZElements]
#DOC-END generated mesh

#DOC-START mesh
meshUserNumber = 1
mesh = iron.Mesh()
generatedMesh.CreateFinish(meshUserNumber,mesh)
#DOC-END mesh

# Create a decomposition for the mesh
#DOC-START decomposition
decompositionUserNumber = 1
decomposition = iron.Decomposition()
decomposition.CreateStart(decompositionUserNumber,mesh)
decomposition.type = iron.DecompositionTypes.CALCULATED
decomposition.numberOfDomains = numberOfComputationalNodes
decomposition.CreateFinish()
#DOC-END decomposition

# Create a field for the geometry
#DOC-START geometry
geometricFieldUserNumber = 1
geometricField = iron.Field()
geometricField.CreateStart(geometricFieldUserNumber,region)
geometricField.meshDecomposition = decomposition
geometricField.ComponentMeshComponentSet(CMISS.FieldVariableTypes.U,1,meshComponentNumber)
geometricField.ComponentMeshComponentSet(CMISS.FieldVariableTypes.U,2,meshComponentNumber)
geometricField.ComponentMeshComponentSet(CMISS.FieldVariableTypes.U,3,meshComponentNumber)
geometricField.CreateFinish()
#DOC-END geometry

# Set geometry from the generated mesh
#DOC-START geometry1
generatedMesh.GeometricParametersCalculate(geometricField)
#DOC-END geometry2

# Create standard Laplace equations set
#DOC-START equationset
equationsSetUserNumber = 1
equationsSetFieldUserNumber = 2
equationsSetField = iron.Field()
equationsSet = iron.EquationsSet()
equationsSetSpecification = [iron.EquationsSetClasses.CLASSICAL_FIELD,
    iron.EquationsSetTypes.LAPLACE_EQUATION,
    iron.EquationsSetSubtypes.STANDARD_LAPLACE]
equationsSet.CreateStart(equationsSetUserNumber,region,geometricField,
    equationsSetSpecification,equationsSetFieldUserNumber,equationsSetField)
equationsSet.CreateFinish()
#DOC-END equationset

# Create dependent field
#DOC-START dependent
dependentFieldUserNumber = 3
dependentField = iron.Field()
equationsSet.DependentCreateStart(dependentFieldUserNumber,dependentField)
dependentField.DOFOrderTypeSet(iron.FieldVariableTypes.U,iron.FieldDOFOrderTypes.SEPARATED)
dependentField.DOFOrderTypeSet(iron.FieldVariableTypes.DELUDELN,iron.FieldDOFOrderTypes.SEPARATED)
equationsSet.DependentCreateFinish()
#DOC-END dependent

# Initialise dependent field
#DOC-START dependent1
componentNumber = 1
initialValue = 0.5
dependentField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,
    componentNumber,initialValue)
#DOC-END dependent1

# Create equations
#DOC-START set
equations = iron.Equations()
equationsSet.EquationsCreateStart(equations)
equations.sparsityType = iron.EquationsSparsityTypes.SPARSE
equations.outputType = iron.EquationsOutputTypes.NONE
equationsSet.EquationsCreateFinish()
#DOC-END set

# Create Laplace problem
#DOC-START problem
problemUserNumber = 1
problem = iron.Problem()
problemSpecification = [iron.ProblemClasses.CLASSICAL_FIELD,
    iron.ProblemTypes.LAPLACE_EQUATION,
    iron.ProblemSubtypes.STANDARD_LAPLACE]
problem.CreateStart(problemUserNumber, problemSpecification)
problem.CreateFinish()
#DOC-END problem

# Create control loops
#DOC-START loops
problem.ControlLoopCreateStart()
problem.ControlLoopCreateFinish()
#DOC-END loops

# Create problem solver
#DOC-START problem solver
solver = iron.Solver()
problem.SolversCreateStart()
problem.SolverGet([iron.ControlLoopIdentifiers.NODE],1,solver)
solver.outputType = iron.SolverOutputTypes.SOLVER
solver.linearType = iron.LinearSolverTypes.ITERATIVE
solver.linearIterativeAbsoluteTolerance = 1.0E-12
solver.linearIterativeRelativeTolerance = 1.0E-12
problem.SolversCreateFinish()
#DOC-END problem solver

# Create solver equations and add equations set to solver equations
#DOC-START solver equations
solver = iron.Solver()
solverEquations = iron.SolverEquations()
problem.SolverEquationsCreateStart()
problem.SolverGet([iron.ControlLoopIdentifiers.NODE],1,solver)
solver.SolverEquationsGet(solverEquations)
solverEquations.sparsityType = iron.SolverEquationsSparsityTypes.SPARSE
equationsSetIndex = solverEquations.EquationsSetAdd(equationsSet)
problem.SolverEquationsCreateFinish()
#DOC-END solver equations

# Create boundary conditions and set first and last nodes to 0.0 and 1.0
#DOC-START BC
boundaryConditions = iron.BoundaryConditions()
solverEquations.BoundaryConditionsCreateStart(boundaryConditions)
firstNodeNumber = 1
nodes = iron.Nodes()
region.NodesGet(nodes)
lastNodeNumber = nodes.numberOfNodes
firstNodeDomain = decomposition.NodeDomainGet(firstNodeNumber,1)
lastNodeDomain = decomposition.NodeDomainGet(lastNodeNumber,1)
if firstNodeDomain == computationalNodeNumber:
    boundaryConditions.SetNode(dependentField,iron.FieldVariableTypes.U,
     1,1,firstNodeNumber,1,iron.BoundaryConditionsTypes.FIXED,0.0)
if lastNodeDomain == computationalNodeNumber:
    boundaryConditions.SetNode(dependentField,iron.FieldVariableTypes.U,
     1,1,lastNodeNumber,1,iron.BoundaryConditionsTypes.FIXED,1.0)
solverEquations.BoundaryConditionsCreateFinish()
#DOC-END BC

# Solve the problem
#DOC-START Solve
problem.Solve()
#DOC-END Solve

# Export results
#DOC-START Export
baseName = "laplace"
dataFormat = "PLAIN_TEXT"
fml = iron.FieldMLIO()
fml.OutputCreate(mesh, "", baseName, dataFormat)
fml.OutputAddFieldNoType(baseName+".geometric", dataFormat, geometricField,
    iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES)
fml.OutputAddFieldNoType(baseName+".phi", dataFormat, dependentField,
    iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES)
fml.OutputWrite("LaplaceExample.xml")
fml.Finalise()
#DOC-END Export

iron.Finalise()
