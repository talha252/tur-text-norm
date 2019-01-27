from libc.float cimport DBL_MAX as DTYPE_MAX
from libc.stdlib cimport malloc, free
cimport cython

ctypedef double DTYPE_t

cdef enum:
    ALPHABET_SIZE = 256


cdef DTYPE_t c_damerau_levenshtein(
	unsigned char* str_a,
	Py_ssize_t len_a,
	unsigned char* str_b,
	Py_ssize_t len_b,
	DTYPE_t threshold,
	DTYPE_t[::1] insert_costs,
	DTYPE_t[::1] delete_costs,
	DTYPE_t[:,::1] delete_adjacent_costs,
	DTYPE_t[::1] delete_repeating_costs,
	DTYPE_t[:,::1] substitute_costs,
	DTYPE_t[:,::1] transpose_costs) nogil


cdef DTYPE_t c_optimal_string_alignment(
	unsigned char* word_m,
	Py_ssize_t m,
	unsigned char* word_n,
	Py_ssize_t n,
	DTYPE_t[::1] insert_costs,
	DTYPE_t[::1] delete_costs,
	DTYPE_t[:,::1] substitute_costs,
	DTYPE_t[:,::1] transpose_costs) nogil


cdef DTYPE_t c_levenshtein(
	unsigned char* word_m,
	Py_ssize_t m,
	unsigned char* word_n,
	Py_ssize_t n,
	DTYPE_t[::1] insert_costs,
	DTYPE_t[::1] delete_costs,
	DTYPE_t[:,::1] substitute_costs) nogil

# Begin helper functions

# Begin Array2D

# Struct that represents a 2D array
ctypedef struct Array2D:
    DTYPE_t* mem
    Py_ssize_t num_rows
    Py_ssize_t num_cols


cdef inline void Array2D_init(
    Array2D* array2d,
    Py_ssize_t num_rows,
    Py_ssize_t num_cols) nogil:
    """
    Initializes an Array2D struct with the given number of rows and columns
    """
    array2d.num_rows = num_rows
    array2d.num_cols = num_cols
    array2d.mem = <DTYPE_t*> malloc(num_rows * num_cols * sizeof(DTYPE_t))


cdef inline void Array2D_del(
    Array2D array2d) nogil:
    """
    Destroys an Array2D struct
    """
    free(array2d.mem)

@cython.profile(False)
@cython.linetrace(False)
cdef inline DTYPE_t Array2D_n1_get(
    Array2D array2d,
    Py_ssize_t row,
    Py_ssize_t col) nogil:
    """
    Takes the row and column index of a (-1)-indexed matrix
    and returns the value at that location
    """
    row += 1
    col += 1
    return array2d.mem[row * array2d.num_cols + col]

@cython.profile(False)
@cython.linetrace(False)
cdef inline DTYPE_t* Array2D_n1_at(
    Array2D array2d,
    Py_ssize_t row,
    Py_ssize_t col) nogil:
    """
    Takes the row and column index of a (-1)-indexed matrix
    and returns a pointer to that location
    """
    row += 1
    col += 1
    return array2d.mem + row * array2d.num_cols + col

@cython.profile(False)
@cython.linetrace(False)
cdef inline DTYPE_t Array2D_0_get(
    Array2D array2d,
    Py_ssize_t row,
    Py_ssize_t col) nogil:
    """
    Takes the row and column index of a 0-indexed matrix
    and returns the value at that location
    """
    return array2d.mem[row * array2d.num_cols + col]

@cython.profile(False)
@cython.linetrace(False)
cdef inline DTYPE_t* Array2D_0_at(
    Array2D array2d,
    Py_ssize_t row,
    Py_ssize_t col) nogil:
    """
    Takes the row and column index of a 0-indexed matrix
    and returns a pointer to that location
    """
    return array2d.mem + row * array2d.num_cols + col

@cython.profile(False)
@cython.linetrace(False)
cdef inline DTYPE_t col_delete_range_cost(
    Array2D d,
    Py_ssize_t start,
    Py_ssize_t end) nogil:
    """
    Calculates the cost incurred by deleting
    characters 'start' to 'end' (inclusive) from 'str1',
    assuming that 'str1' is 1-indexed.

    Works since column 0 of 'd' is the cumulative sums
    of the deletion costs of the characters in str1.

    This function computes the range sum by computing the difference
    between the cumulative sums at each end of the range.
    """
    return Array2D_n1_get(d, end, 0) - Array2D_n1_get(d, start - 1, 0)

@cython.profile(False)
@cython.linetrace(False)
cdef inline DTYPE_t row_insert_range_cost(
    Array2D d,
    Py_ssize_t start,
    Py_ssize_t end) nogil:
    """
    Calculates the cost incurred by inserting
    characters 'start' to 'end' (inclusive) from 'str2',
    assuming that 'str2' is 1-indexed.

    Works since row 0 of 'd' is the cumulative sums
    of the insertion costs of the characters in str2.

    This function computes the range sum by computing the difference
    between the cumulative sums at each end of the range.
    """
    return Array2D_n1_get(d, 0, end) - Array2D_n1_get(d, 0, start - 1)

# End Array2D

@cython.profile(False)
@cython.linetrace(False)
cdef inline unsigned char str_1_get(unsigned char* s, Py_ssize_t i) nogil:
    """
    Takes an index of a 1-indexed string
    and returns that character
    """
    return s[i - 1]

# End helper functions

