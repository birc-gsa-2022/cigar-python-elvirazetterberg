"""A module for translating between edit strings and cigar strings."""

import re


def split_pairs(cigar: str) -> list[tuple[int, str]]:
    """Split a CIGAR string into a list of integer-operation pairs.

    Args:
        cigar (str): A CIGAR string

    Returns:
        list[tuple[int, str]]: A list of pairs, where the first element is
        an integer and the second an edit operation.

    >>> split_pairs("1M1D6M1I4M")
    [(1, 'M'), (1, 'D'), (6, 'M'), (1, 'I'), (4, 'M')]

    """
    # In a more sane language, we could get a faster solution by identifying
    # the part of a block that is all digits and then translate that
    # into an integer, but the relative speed of pure Python and its
    # regular expressions make this a reasonable solution.
    return [(int(i), op) for i, op in re.findall(r"(\d+)([^\d]+)", cigar)]


def cigar_to_edits(cigar: str) -> str:
    """Expand the compressed CIGAR encoding into the full list of edits.

    Args:
        cigar (str): A CIGAR string

    Returns:
        str: The edit operations the CIGAR string describes.

    >>> cigar_to_edits("1M1D6M1I4M")
    'MDMMMMMMIMMMM'

    """
    num = 0
    edits = []
    if len(cigar) == 0:
        return ''

    for i,fig in enumerate(cigar):
        if i%2 == 0:
            num = int(fig)
            continue
        else:
            edits.append(fig*num)     

    return edits


def split_blocks(x: str) -> list[str]:
    """Split a string into blocks of equal character.

    Args:
        x (str): A string, but we sorta think it would be edits.

    Returns:
        list[str]: A list of blocks.

    >>> split_blocks('MDMMMMMMIMMMM')
    ['M', 'D', 'MMMMMM', 'I', 'MMMM']

    """
    # In any other language, this would likely not be the most efficient
    # approach to this, but since re.findall calls into C, it is faster
    # than implementing a more reasonable algorithm in pure Python.
    return [m[0] for m in re.findall(r"((.)\2*)", x)]


def edits_to_cigar(edits: str) -> str:
    """Encode a sequence of edits as a CIGAR.

    Args:
        edits (str): A sequence of edit operations

    Returns:
        str: The CIGAR encoding of edits.

    >>> edits_to_cigar('MDMMMMMMIMMMM')
    '1M1D6M1I4M'

    """

    def _summation(cont_list):
        if len(cont_list) == 0:
            return ''
        else:
            return ''.join([str(len(cont_list)), cont_list[0]])

    
    if len(edits) == 0:
        return ''

    temp = []
    cigar = []
    for i,l in enumerate(edits):
        if l == edits[-1]:
            temp.append(l)
            cigar.append(_summation(temp))
        else:
            if l == edits[i+1]:
                temp.append(edits[i+1])
            else:
                temp.append(l)
                cigar.append(_summation(temp))
                temp = []

    # cigar = []
    # i = 0
    # temp = edits[0]
    # while True:
    #     if i == len()
    #     if temp == edits[-1]
    #         cigar.append(''.join([temp, '1']))
    #         break
    #     i += 1
    #     counter = 0
    #     if temp != edits[i]:
    #         cigar.append(''.join([temp, '1']))
    #     elif temp == edits[i]:
    #         while temp == edits[i]:
    #             counter += 1
    #             i += 1
    #         cigar.append(''.join([temp, str(counter)]))
    #     temp = edits[i]
    
    final = ''.join(cigar)
    
    return final
