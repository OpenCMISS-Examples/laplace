add_executable(laplace_fortran laplace.F90)

target_link_libraries(laplace_fortran PRIVATE opencmisslibs mpi)

install(TARGETS laplace_fortran DESTINATION bin)
