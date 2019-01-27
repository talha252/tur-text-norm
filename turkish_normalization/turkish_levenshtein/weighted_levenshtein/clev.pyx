#!python
# cython: language_level=3, boundscheck=False, wraparound=False, embedsignature=True, linetrace=True, c_string_type=str, c_string_encoding=iso-8859-9
# distutils: define_macros=CYTHON_TRACE_NOGIL=1

from cython.view cimport array as cvarray
from .clev cimport DTYPE_t, DTYPE_MAX, ALPHABET_SIZE

from libc.stdio cimport printf


cyarr = cvarray(shape=(ALPHABET_SIZE,), itemsize=sizeof(double), format="d")
cdef DTYPE_t[::1] unit_array = cyarr
unit_array[:] = 1

cymatrix = cvarray(shape=(ALPHABET_SIZE, ALPHABET_SIZE), itemsize=sizeof(double), format="d")
cdef DTYPE_t[:,::1] unit_matrix = cymatrix
unit_matrix[:, :] = 1

cdef DTYPE_t[::1] _insert_costs = unit_array
cdef DTYPE_t[:,::1] _delete_adjacent_costs = unit_matrix
cdef DTYPE_t[::1] _delete_costs = unit_array
cdef DTYPE_t[::1] _delete_repeating_costs = unit_array
cdef DTYPE_t[:,::1] _substitute_costs = unit_matrix
cdef DTYPE_t[:,::1] _transpose_costs = unit_matrix

def set_costs(insert_costs=None, substitute_costs=None, delete_costs=None, delete_adjacent_costs=None, delete_repeating_costs=None, transpose_costs=None):
    global _insert_costs, _delete_adjacent_costs, _delete_costs, _delete_repeating_costs, _substitute_costs, _transpose_costs
    if insert_costs is not None:
        _insert_costs = insert_costs

    if substitute_costs is not None:
        _substitute_costs = substitute_costs

    if delete_costs is not None:
        _delete_costs = delete_costs

    if delete_adjacent_costs is not None:
        _delete_adjacent_costs = delete_adjacent_costs

    if delete_repeating_costs is not None:
        _delete_repeating_costs = delete_repeating_costs

    if transpose_costs is not None:
        _transpose_costs = transpose_costs


def damerau_levenshtein(
    bytes str1,
    bytes str2,
    DTYPE_t threshold=DTYPE_MAX,
    ):
    return c_damerau_levenshtein(
        str1, len(str1),
        str2, len(str2),
        threshold,
        _insert_costs,
        _delete_costs,
        _delete_adjacent_costs,
        _delete_repeating_costs,
        _substitute_costs,
        _transpose_costs
    )

dam_lev = damerau_levenshtein


cdef DTYPE_t c_damerau_levenshtein(
    unsigned char* str1, Py_ssize_t len1,
    unsigned char* str2, Py_ssize_t len2,
    DTYPE_t threshold,
    DTYPE_t[::1] insert_costs,
    DTYPE_t[::1] delete_costs,
    DTYPE_t[:,::1] delete_adjacent_costs,
    DTYPE_t[::1] delete_repeating_costs,
    DTYPE_t[:,::1] substitute_costs,
    DTYPE_t[:,::1] transpose_costs) nogil:
    """
    https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Distance_with_adjacent_transpositions
    """
    cdef:
        Py_ssize_t[ALPHABET_SIZE] da

        Py_ssize_t i, j
        unsigned char char_i, char_j, char_p
        DTYPE_t cost, del_cost, ret_val, current_total_cost, min_total_cost
        Py_ssize_t db, k, l
        Array2D d

    Array2D_init(&d, len1 + 2, len2 + 2)
    # initialize 'da' to all 0
    for i in range(ALPHABET_SIZE):
        da[i] = 0

    # fill row (-1) and column (-1) with 'DTYPE_MAX'
    Array2D_n1_at(d, -1, -1)[0] = DTYPE_MAX
    for i in range(0, len1 + 1):
        Array2D_n1_at(d, i, -1)[0] = DTYPE_MAX
    for j in range(0, len2 + 1):
        Array2D_n1_at(d, -1, j)[0] = DTYPE_MAX

    # fill row 0 and column 0 with insertion and deletion costs
    Array2D_n1_at(d, 0, 0)[0] = 0
    for i in range(1, len1 + 1):
        char_i = str_1_get(str1, i)
        cost = delete_costs[char_i]
        Array2D_n1_at(d, i, 0)[0] = Array2D_n1_get(d, i - 1, 0) + cost
    for j in range(1, len2 + 1):
        char_j = str_1_get(str2, j)
        cost = insert_costs[char_j]
        Array2D_n1_at(d, 0, j)[0] = Array2D_n1_get(d, 0, j - 1) + cost

    char_p = str_1_get(str1, 2)
    # fill DP array
    for i in range(1, len1 + 1):
        char_i = str_1_get(str1, i)
        db = 0
        min_total_cost = DTYPE_MAX
        for j in range(1, len2 + 1):
            char_j = str_1_get(str2, j)
            k = da[char_j]
            l = db
            if char_i == char_j:
                cost = 0
                db = j
            else:
                cost = substitute_costs[char_i, char_j]
            # if we want to delete a repeating char, then use the repeating cost table
            if char_i == char_p:
                del_cost = delete_repeating_costs[char_i]
            elif char_i == char_j and (i - j == 1 or j - i == 1):
                # this only works for distance of one to prevent (bu --> bunu second u was consired as first u previously)
                # if currently selected characters are the same then it's possible that
                # adjacent character of current character might be inserted previously
                # then we subtract insertion cost of that character and replace with delete_adjancency_cost
                # of adjacent character.
                # for example: geklecem --> gelecem (k inserted previosly)
                del_cost = delete_adjacent_costs[char_i, char_p] - insert_costs[char_p]
            else:
                # it's possible that adjacent character added after than current char
                # for example:  gelkecem -> gelecem
                del_cost = min(delete_costs[char_i], delete_adjacent_costs[char_i, char_j])

            current_total_cost = min(
                Array2D_n1_get(d, i - 1, j - 1) + cost,                # equal/substitute
                Array2D_n1_get(d, i, j - 1) + insert_costs[char_j],    # insert
                Array2D_n1_get(d, i - 1, j) + del_cost,                # delete/delete repeating/delete adjancent
                Array2D_n1_get(d, k - 1, l - 1) +                      # transpose
                    col_delete_range_cost(d, k + 1, i - 1) +                    # delete chars in between
                    transpose_costs[str_1_get(str1, k), str_1_get(str1, i)] +   # transpose chars
                    row_insert_range_cost(d, l + 1, j - 1)                      # insert chars in between
            )
            
            Array2D_n1_at(d, i, j)[0] = current_total_cost
            if current_total_cost < min_total_cost:
                min_total_cost = current_total_cost
            # printf("---------------------------------\n")
            # printf("i: %d, j: %d, COST: %.2f\n", i, j, current_total_cost)
            # printf('char_i: %d, char_j: %d, char_p: %d\n', char_i, char_j, char_p)
            # printf('ins_cost: %.2f, ins_adj_cost: %.2f\n', insert_costs[char_j], delete_adjacent_costs[char_i, char_j])
        if min_total_cost > threshold: # if the current cost is bigger than threshold
            Array2D_del(d)
            return -1 # return meaningless value
        da[char_i] = i
        char_p = char_i

    ret_val = Array2D_n1_get(d, len1, len2)
    if ret_val > threshold: # sometimes threshold doesn't apply, for those use this if
        Array2D_del(d)
        return -1
    Array2D_del(d)
    return ret_val


def optimal_string_alignment(
    unsigned char* str1,
    unsigned char* str2,
    DTYPE_t[::1] insert_costs=None,
    DTYPE_t[::1] delete_costs=None,
    DTYPE_t[:,::1] substitute_costs=None,
    DTYPE_t[:,::1] transpose_costs=None):
    """
    Calculates the Optimal String Alignment distance between str1 and str2,
    provided the costs of inserting, deleting, and substituting characters.
    The costs default to 1 if not provided.

    For convenience, this function is aliased as clev.osa().

    :param str str1: first string
    :param str str2: second string
    :param np.ndarray insert_costs: a numpy array of np.float64 (C doubles) of length 128 (0..127),
        where insert_costs[i] is the cost of inserting ASCII character i
    :param np.ndarray delete_costs: a numpy array of np.float64 (C doubles) of length 128 (0..127),
        where delete_costs[i] is the cost of deleting ASCII character i
    :param np.ndarray substitute_costs: a 2D numpy array of np.float64 (C doubles) of dimensions (128, 128),
        where substitute_costs[i, j] is the cost of substituting ASCII character i with
        ASCII character j
    :param np.ndarray transpose_costs: a 2D numpy array of np.float64 (C doubles) of dimensions (128, 128),
        where transpose_costs[i, j] is the cost of transposing ASCII character i with
        ASCII character j, where character i is followed by character j in the string
    """
    if insert_costs is None:
        insert_costs = unit_array
    if delete_costs is None:
        delete_costs = unit_array
    if substitute_costs is None:
        substitute_costs = unit_matrix
    if transpose_costs is None:
        transpose_costs = unit_matrix

    s1 = str(str1).encode()  
    s2 = str(str2).encode()   

    return c_optimal_string_alignment(
        s1, len(s1),
        s2, len(s2),
        insert_costs,
        delete_costs,
        substitute_costs,
        transpose_costs
    )

osa = optimal_string_alignment


cdef DTYPE_t c_optimal_string_alignment(
    unsigned char* str1, Py_ssize_t len1,
    unsigned char* str2, Py_ssize_t len2,
    DTYPE_t[::1] insert_costs,
    DTYPE_t[::1] delete_costs,
    DTYPE_t[:,::1] substitute_costs,
    DTYPE_t[:,::1] transpose_costs) nogil:
    """
    https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance
    """
    cdef:
        Py_ssize_t i, j
        unsigned char char_i, char_j, prev_char_i, prev_char_j
        DTYPE_t ret_val
        Array2D d

    Array2D_init(&d, len1 + 1, len2 + 1)

    # fill row 0 and column 0 with insertion and deletion costs
    Array2D_0_at(d, 0, 0)[0] = 0
    for i in range(1, len1 + 1):
        char_i = str_1_get(str1, i)
        Array2D_0_at(d, i, 0)[0] = Array2D_0_get(d, i - 1, 0) + delete_costs[char_i]
    for j in range(1, len2 + 1):
        char_j = str_1_get(str2, j)
        Array2D_0_at(d, 0, j)[0] = Array2D_0_get(d, 0, j - 1) + insert_costs[char_j]

    # fill DP array
    for i in range(1, len1 + 1):
        char_i = str_1_get(str1, i)
        for j in range(1, len2 + 1):
            char_j = str_1_get(str2, j)
            if char_i == char_j:  # match
                Array2D_0_at(d, i, j)[0] = Array2D_0_get(d, i - 1, j - 1)
            else:
                Array2D_0_at(d, i, j)[0] = min(
                    Array2D_0_get(d, i - 1, j) + delete_costs[char_i],  # deletion
                    Array2D_0_get(d, i, j - 1) + insert_costs[char_j],  # insertion
                    Array2D_0_get(d, i - 1, j - 1) + substitute_costs[char_i, char_j]  # substitution
                )

            if i > 1 and j > 1:
                prev_char_i = str_1_get(str1, i - 1)
                prev_char_j = str_1_get(str2, j - 1)
                if char_i == prev_char_j and prev_char_i == char_j:  # transpose
                    Array2D_0_at(d, i, j)[0] = min(
                        Array2D_0_get(d, i, j),
                        Array2D_0_get(d, i - 2, j - 2) + transpose_costs[prev_char_i, char_i]
                    )

    ret_val = Array2D_0_get(d, len1, len2)
    Array2D_del(d)
    return ret_val


def levenshtein(
    unsigned char* str1,
    unsigned char* str2,
    DTYPE_t[::1] insert_costs=None,
    DTYPE_t[::1] delete_costs=None,
    DTYPE_t[:,::1] substitute_costs=None):
    """
    Calculates the Levenshtein distance between str1 and str2,
    provided the costs of inserting, deleting, and substituting characters.
    The costs default to 1 if not provided.

    For convenience, this function is aliased as clev.lev().

    :param str str1: first string
    :param str str2: second string
    :param np.ndarray insert_costs: a numpy array of np.float64 (C doubles) of length 128 (0..127),
        where insert_costs[i] is the cost of inserting ASCII character i
    :param np.ndarray delete_costs: a numpy array of np.float64 (C doubles) of length 128 (0..127),
        where delete_costs[i] is the cost of deleting ASCII character i
    :param np.ndarray substitute_costs: a 2D numpy array of np.float64 (C doubles) of dimensions (128, 128),
        where substitute_costs[i, j] is the cost of substituting ASCII character i with
        ASCII character j

    """
    if insert_costs is None:
        insert_costs = unit_array
    if delete_costs is None:
        delete_costs = unit_array
    if substitute_costs is None:
        substitute_costs = unit_matrix

    s1 = str(str1).encode()
    s2 = str(str2).encode()  

    return c_levenshtein(
        s1, len(s1),
        s2, len(s2),
        insert_costs,
        delete_costs,
        substitute_costs
    )

lev = levenshtein


cdef DTYPE_t c_levenshtein(
    unsigned char* str1, Py_ssize_t len1,
    unsigned char* str2, Py_ssize_t len2,
    DTYPE_t[::1] insert_costs,
    DTYPE_t[::1] delete_costs,
    DTYPE_t[:,::1] substitute_costs) nogil:
    """
    https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm
    """
    cdef:
        Py_ssize_t i, j
        unsigned char char_i, char_j
        DTYPE_t ret_val
        Array2D d

    Array2D_init(&d, len1 + 1, len2 + 1)

    Array2D_0_at(d, 0, 0)[0] = 0
    for i in range(1, len1 + 1):
        char_i = str_1_get(str1, i)
        Array2D_0_at(d, i, 0)[0] = Array2D_0_get(d, i - 1, 0) + delete_costs[char_i]
    for j in range(1, len2 + 1):
        char_j = str_1_get(str2, j)
        Array2D_0_at(d, 0, j)[0] = Array2D_0_get(d, 0, j - 1) + insert_costs[char_j]

    for i in range(1, len1 + 1):
        char_i = str_1_get(str1, i)
        for j in range(1, len2 + 1):
            char_j = str_1_get(str2, j)
            if char_i == char_j:  # match
                Array2D_0_at(d, i, j)[0] = Array2D_0_get(d, i - 1, j - 1)
            else:
                Array2D_0_at(d, i, j)[0] = min(
                    Array2D_0_get(d, i - 1, j) + delete_costs[char_i],
                    Array2D_0_get(d, i, j - 1) + insert_costs[char_j],
                    Array2D_0_get(d, i - 1, j - 1) + substitute_costs[char_i, char_j]
                )

    ret_val = Array2D_0_get(d, len1, len2)
    Array2D_del(d)
    return ret_val
