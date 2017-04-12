# Add example executable
add_executable(laplace_c src/CExample.c)

# Link to opencmiss
# -----------------
#
# This simply uses the 'opencmisslibs' target created by finding the OpenCMISSLibs package earlier.
#
# Alternatively, you can also directly invoke 'find_package(Iron <IRON_VERSION>)' to explicitly
# require that version.  If you do this you will also need to change the target link library from
# 'opencmisslibs' to 'iron'. 
target_link_libraries(laplace_c PRIVATE opencmisslibs)

# Add a simple test that runs the executable
add_test(Laplace_C laplace_c)
# Helper function defined in OCMiscFunctions.cmake
add_opencmiss_environment(Laplace_C)

# Add an install target to place the executable in the install tree.
install(TARGETS laplace_c
    DESTINATION bin)
