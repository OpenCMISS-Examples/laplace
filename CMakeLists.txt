# OpenCMISS (Open Continuum Mechanics, Imaging, Signal processing and System identification)
# is a mathematical modelling environment that enables the application of finite element
# analysis techniques to a variety of complex bioengineering problems.
# 
# The OpenCMISS project website can be found at http://www.opencmiss.org
#
# --- Welcome! ---
# This is the template for main build files for OpenCMISS examples using the CMake build system
#
# For most situations, all you need to do is set the OPENCMISS_INSTALL_DIR to the
# desired/given OpenCMISS install directory.
#
# *Note that you may also define OPENCMISS_INSTALL_DIR in your environment!*
#
# For more information see http://www.opencmiss.org/documentation

############################## Preparation ##############################

# Include the OpenCMISS initalisation & macro definition file.
include("./OpenCMISS.cmake")

# Project setup
# -------------
# Change the project name and minimum required CMake version here if required.
# 
# .. note::
#
#     The OC_INIT script additionally ensures the CMake version is sufficienty new
#     for the found OpenCMISS installation
cmake_minimum_required(VERSION 3.3 FATAL_ERROR)
project(OpenCMISS-Example VERSION 1.0 LANGUAGES C)
enable_language(Fortran OPTIONAL)
enable_testing()

# Initialise OpenCMISS
# --------------------
#
# The OC_INIT function takes the following arguments:
#
# OC_INIT(VERSION [, COMPONENT [, ...]])
#
#    VERSION: The minimum OpenCMISS version required for this example
#    COMPONENT: One or more OpenCMISS components that are required.
#               Currently available: Iron Zinc
#
# This function creates a link target 'opencmiss' that contains references to the requested OpenCMISS components.
# For Iron, it also adds the necessary MPI information - no further find_package(MPI ..) and setting of extra include
# paths needed ;-)

OC_INIT(1.1 Iron)

############################## Actual example code ##############################

add_subdirectory(C)
if (CMAKE_Fortran_COMPILER)
    add_subdirectory(Fortran)
endif()
