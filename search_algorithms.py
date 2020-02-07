# Naive search iterates i over the elements in txt
# At each position in txt it checks txt[i] == pat[0], txt[i+1] == pat[1], txt[i + M - 1] == pat[M - 1]
# If any of these return false, there is no match and it increments i
# If they all match then it stores i in result and increments i

def naiveSearch(pat, txt):
    M = len(pat)
    N = len(txt)

    result = []

    i = 0

    # Iterate over all possible starting places for a match
    while (i <= N - M):
        j = 0
        
        # Iterate over the pattern and check for match
        while (j < M):
            if pat[j] != txt[i + j]:
                break

            j += 1
            
            if j == M:
                #print("Pattern at i = " + str(i))
                result.append(i)

        i += 1

    return result



# The KMP algorithm attempts to reduce the number of elements which are compared more than once
# Rather than matching the whole of the pattern at the next index, it only matches those parts of the pattern
# which aren't guarunteed to match. See https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/

def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)

    lps = M*[0]
    
    computeLPSArray(pat, lps)

    j = 0 # Index for pat
    i = 0 # Index for txt

    result = []

    while (i < N):
        if txt[i] == pat[j]:
            # If there is a match, compare next elements
            i += 1
            j += 1

        if j == M:
            # If there is no next element in pat
            # the whole pattern has matched

            #print("Pattern at i = " +  str(i - M))
            result.append(i - M)

            # Move j to the end of the longest prefix which is also a suffix
            # We have already matched this as a suffix, so we needn't match it as a prefix
            j = lps[M - 1]
        
        elif i < N and txt[i] != pat[j]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1

    return result
                


# A helper function for the KMP search. Given an array, we record at position i
# the size of the largest prefix of pat[:i] which is also a suffix of pat[:i]
def computeLPSArray(pat, lps):
    M = len(pat)

    # There is no proper suffix of an array of length 1
    lps[0] = 0

    # Index for prefix
    j = 0

    # Index for suffix
    i = 1

    while (i < M):
        # We assume that pat[i - k] == pat[j - k] for k = 1...j
        if pat[i] == pat[j]:
            # If the pattern at location i matches the pattern at location j
            # then pat[i - k] == pat[j - k] for k = 0...j
            j += 1
            lps[i] = j

            i += 1

        else:
            if j != 0:
                # Since we know that pat[i] != pat[j], we use the assumption that pat[i - k] == pat[j - k] for k = 1...j
                # to skip checking cases we know will already match. Note that this maintains the loop invariant
                # We move the prefix index to the longest proper prefix of pat[:j-1] which is also a suffix
                # In the next iteration we check if this prefix can be extended
                j = lps[j - 1]

            else:
                # We have tried all possible prefixes up down to the one element prefix
                # None match, so we set lps[i] = 0 and increment
                lps[i] = 0
                i += 1



