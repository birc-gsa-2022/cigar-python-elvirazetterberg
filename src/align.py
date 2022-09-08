"""A module for translating between alignments and edits sequences."""


def get_edits(p: str, q: str) -> tuple[str, str, str]:
    """Extract the edit operations from a pairwise alignment.

    Args:
        p (str): The first row in the pairwise alignment.
        q (str): The second row in the pairwise alignment.

    Returns:
        str: The list of edit operations as a string.

    >>> get_edits('ACCACAGT-CATA', 'A-CAGAGTACAAA')
    ('ACCACAGTCATA', 'ACAGAGTACAAA', 'MDMMMMMMIMMMM')

    """
    assert len(p) == len(q)


    if p == '':
        return '', '', ''
    
    cigar = []
    for i in range(len(p)):
        if p[i] == q[i]:
            cigar.append('M')
        elif p[i] == '-':
            cigar.append('I')
        else:
            cigar.append('D')

    p = p.replace('-', '')
    q = q.replace('-', '')
    cigar = ''.join(cigar)
    
    return p, q, cigar


def local_align(p: str, x: str, i: int, edits: str) -> tuple[str, str]:
    """Align two sequences from a sequence of edits.

    Args:
        p (str): The read string we have mapped against x
        x (str): The longer string we have mapped against
        i (int): The location where we have an approximative match
        edits (str): The list of edits to apply, given as a string

    Returns:
        tuple[str, str]: The two rows in the pairwise alignment

    >>> local_align("ACCACAGTCATA", "GTACAGAGTACAAA", 2, "MDMMMMMMIMMMM")
    ('ACCACAGT-CATA', 'A-CAGAGTACAAA')

    """
    if p == '' and x == '' and edits == '':
        return '', ''
    elif edits == len(edits)*'M':
        return p, x
    else:
        pnew = p
        xnew = x[i:]
        for j in range(i, len(edits)):
            if edits[j] == 'M':
                continue
            elif edits[j] == 'D':
                xnew = '-'.join([xnew[:j], xnew[j:]])
            else:
                pnew = '-'.join([pnew[:j], pnew[j:]])

        return pnew, xnew

def align(p: str, q: str, edits: str) -> tuple[str, str]:
    """Align two sequences from a sequence of edits.

    Args:
        p (str): The first sequence to align.
        q (str): The second sequence to align
        edits (str): The list of edits to apply, given as a string

    Returns:
        tuple[str, str]: The two rows in the pairwise alignment

    >>> align("ACCACAGTCATA", "ACAGAGTACAAA", "MDMMMMMMIMMMM")
    ('ACCACAGT-CATA', 'A-CAGAGTACAAA')

    """
    if p == '' and q == '' and edits == '':
        return '', ''
    elif edits == len(edits)*'M':
        return p, q
    else:
        pnew = p
        qnew = q
        for j in range(len(edits)):
            if edits[j] == 'M':
                continue
            elif edits[j] == 'D':
                qnew = '-'.join([qnew[:j], qnew[j:]])
            else:
                pnew = '-'.join([pnew[:j], pnew[j:]])

        return pnew, qnew


def edit_dist(p: str, x: str, i: int, edits: str) -> int:
    """Get the distance between p and the string that starts at x[i:]
    using the edits.

    Args:
        p (str): The read string we have mapped against x
        x (str): The longer string we have mapped against
        i (int): The location where we have an approximative match
        edits (str): The list of edits to apply, given as a string

    Returns:
        int: The distance from p to x[i:?] described by edits

    >>> edit_dist("accaaagta", "cgacaaatgtcca", 2, "MDMMIMMMMIIM")
    5
    """
    if p == '' or x == '':
        return 0
    
    pnew, xnew = local_align(p, x, i, edits)

    counter = 0
    for j in range(len(pnew)):
        if pnew[j] == '-' or xnew[j] == '-':
            counter += 1
            continue
        elif pnew[j] != xnew[j]:
            counter += 1
            continue

    return counter
