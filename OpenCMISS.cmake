###########################
# *DO NOT CHANGE THIS FILE*
###########################
#
# Prepares the use of OpenCMISS and defines macros to find the CMake-built OpenCMISS software suite.
#
# There need to be two parts as some code has to be run *before* and *after* the CMake project() command is issued.
# 

################################################################################
# Inclusion part - before "project()" command
########
#
# Thus far this
#     - Searches if OPENCMISS_INSTALL_DIR or OPENCMISS_SDK_DIR are defined directly
#       or in the environment. On Windows, the Registry is searched additionally for installed SDKs.
#     - Includes the toolchain config script of the found opencmiss installation

# Convenience: The OPENCMISS_INSTALL_DIR may also be defined in the environment and various other places
if (DEFINED OPENCMISS_INSTALL_DIR)
    get_filename_component(OPENCMISS_INSTALL_DIR "${OPENCMISS_INSTALL_DIR}" ABSOLUTE)
    if (EXISTS OPENCMISS_INSTALL_DIR)
        message(STATUS "Using specified installation directory '${OPENCMISS_INSTALL_DIR}'")
    else()
        message(WARNING "The specified OPENCMISS_INSTALL_DIR '${OPENCMISS_INSTALL_DIR}' does not exist. Skipping.")
        unset(OPENCMISS_INSTALL_DIR)
    endif()
endif()
if(NOT OPENCMISS_INSTALL_DIR AND NOT "$ENV{OPENCMISS_INSTALL_DIR}" STREQUAL "")
    file(TO_CMAKE_PATH "$ENV{OPENCMISS_INSTALL_DIR}" OPENCMISS_INSTALL_DIR)
    get_filename_component(OPENCMISS_INSTALL_DIR "${OPENCMISS_INSTALL_DIR}" ABSOLUTE)
    if (EXISTS OPENCMISS_INSTALL_DIR)
        message(STATUS "Using environment installation directory '${OPENCMISS_INSTALL_DIR}'")
    else()
        message(WARNING "The environment variable OPENCMISS_INSTALL_DIR='${OPENCMISS_INSTALL_DIR}' contains an invalid path. Skipping.")
        unset(OPENCMISS_INSTALL_DIR)
    endif()
endif()
if (NOT OPENCMISS_INSTALL_DIR AND DEFINED OPENCMISS_SDK_DIR)
    get_filename_component(OPENCMISS_SDK_DIR "${OPENCMISS_SDK_DIR}" ABSOLUTE)
    if (EXISTS OPENCMISS_SDK_DIR)
        message(STATUS "Using SDK installation directory: ${OPENCMISS_SDK_DIR}")
        set(OPENCMISS_INSTALL_DIR "${OPENCMISS_SDK_DIR}")
    else()
        message(WARNING "The specified OPENCMISS_SDK_DIR '${OPENCMISS_SDK_DIR}' does not exist. Skipping.")
        unset(OPENCMISS_INSTALL_DIR)
    endif()
endif()    
if(NOT OPENCMISS_INSTALL_DIR AND NOT "$ENV{OPENCMISS_SDK_DIR}" STREQUAL "")
    file(TO_CMAKE_PATH "$ENV{OPENCMISS_SDK_DIR}" OPENCMISS_SDK_DIR)
    get_filename_component(OPENCMISS_SDK_DIR "${OPENCMISS_SDK_DIR}" ABSOLUTE)
    if (EXISTS OPENCMISS_SDK_DIR)
        message(STATUS "Using environment SDK installation directory: ${OPENCMISS_SDK_DIR}")
        set(OPENCMISS_INSTALL_DIR "${OPENCMISS_SDK_DIR}")
    else()
        message(WARNING "The environment variable OPENCMISS_SDK_DIR='${OPENCMISS_SDK_DIR}' contains an invalid path. Skipping.")
        unset(OPENCMISS_INSTALL_DIR)
    endif()
endif()
# On windows: check the registry for installed OpenCMISS SDKs
if(NOT OPENCMISS_INSTALL_DIR AND WIN32)
    foreach(ROOT HKEY_CURRENT_USER HKEY_LOCAL_MACHINE)
        foreach(PACKAGE OpenCMISSUserSDK OpenCMISSDeveloperSDK)
            set(_REG_KEY "[${ROOT}\\Software\\Auckland Bioengineering Institute\\${PACKAGE};Path]")
            get_filename_component(OPENCMISS_INSTALL_DIR "${_REG_KEY}" ABSOLUTE)
            #message(STATUS "Trying registry key ${_REG_KEY}: ${OPENCMISS_INSTALL_DIR}")
            if (OPENCMISS_INSTALL_DIR)
                #set(OPENCMISS_INSTALL_DIR "${OPENCMISS_INSTALL_DIR}" CACHE STRING "Installed SDK" FORCE)
                message(STATUS "Found ${PACKAGE} in Windows registry key ${_REG_KEY}")
                break()
            else()
                unset(OPENCMISS_INSTALL_DIR)   
            endif()         
        endforeach()
        if (OPENCMISS_INSTALL_DIR)
            break()
        endif()
    endforeach()
endif()

# Use the OpenCMISS scripts to also allow choosing a separate toolchain
# This file is located at the opencmiss installation rather than the local example
# as it avoids file replication and makes maintenance much easier
if (TOOLCHAIN)
    set(_OCTC ${OPENCMISS_INSTALL_DIR}/cmake/OCToolchainCompilers.cmake)
    if (EXISTS "${_OCTC}")
        include(${_OCTC})
    else()
        message(WARNING "TOOLCHAIN specified but OpenCMISS config script could not be found at ${_OCTC}. Using CMake defaults.")
    endif()
    unset(_OCTC)
endif()

################################################################################
# Initialization part - after "project()" command
########
# Initializes the use of OpenCMISS and its components.
# Returns a target "opencmiss" that can be used as link library within your application code.
#
# Arguments:
#    VERSION: The minimum OpenCMISS version to look for.
#    COMPONENT1: At least one OpenCMISS component you want to use.
#        Available are Iron, Iron-C and Zinc thus far.
#    [, COMPONENT2,...]: Any more components of OpenCMISS you require to be available.
#
# Thus far this
#     - Adds OPENCMISS_INSTALL_DIR to the CMAKE_PREFIX_PATH
#     - Issues find_package(OpenCMISS) call to locate a matching OpenCMISS installation
#       Matches Version and selected architecture path (Toolchain, MPI, Multithreading, ...)
#     - Adds some necessary flags 
macro(OC_INIT VERSION COMPONENT)

    # For systems where it still works
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
    
    # One could specify CMAKE_PREFIX_PATH directly, however using OPENCMISS_INSTALL_DIR will be more intuitive
    list(APPEND CMAKE_PREFIX_PATH ${OPENCMISS_INSTALL_DIR})
    
    # Look for a matching OpenCMISS!
    find_package(OpenCMISS ${VERSION} REQUIRED ${COMPONENT} ${ARGN} CONFIG)
    
    # On some platforms (windows), we do not have the mpi.mod file or it could not be compatible for inclusion
    # This variable is set by the FindMPI.cmake module in OPENCMISS_INSTALL_DIR/cmake/OpenCMISSExtraFindModules
    if (NOT MPI_Fortran_MODULE_COMPATIBLE)
        add_definitions(-DNOMPIMOD)
    endif()
    
    # Turn on Fortran preprocessing (#include directives)
    if (MSVC)
        set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} /fpp")
    else()
        set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -cpp")
    endif()
endmacro()
