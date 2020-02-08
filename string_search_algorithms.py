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
# Rather than matching the whole of the pattern at the next index, it ignores those parts of the pattern
# which are guarunteed to match. More precisely, suppose elements 0,...,j-1 in the pattern match with the text,
# while element j does not match with element i + j in the text. In the naive algorithm, we jump back to
# pat[0] and txt[i + 1]. Now, if j > 3, the statement pat[:3] == txt[i+1:i+4] is precisely the statement that 
# pat[:3] == pat[1:4], because we already know from the previous iteration that pat[1:4] == txt[i+1:i+4]. Thus,
# the next reasonable comparison is pat[3] with txt[i + 4]. This is the key to the KMP algorithm: that
# certain comparisons can be skipped based purely on j and the pattern.

# To further explore which data is required to compute the next comparison, consider again the situation immediately
# after txt[i + j] fails to match pat[j]. For the same reason as above, any k = 1,...,j-1 with pat[:j - k] == txt[i + k:i + j]
# must have pat[k:j] == pat[:j - k]. That is, there must be a suffix pat[:j] which is also a prefix of pat[:j]. If there is such
# prefix/suffix, the next reasonable point to check is txt[i + j] with pat[j - k] (that is, we need to know k, the length of
# the prefix/suffix). Of course, it may occur that there are multiple such prefix/suffix pairs for a given j; in this
# case, we seek the length of the longest one, as this is the prefix/suffix pair which (implicitely) places pat[0]
# against the earliest element in txt.

# Such suffix which are also prefix are called lps - longest proper prefix suffix (proper because at length j we only consider prefix
# of length less than j). Since the length of the lps can be pre-computed, the KMP algorithm offers significant speedup over the
# naive.

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

        if pat[i] == pat[j]: # then pat[i - k] == pat[j - k] for k = 0...j
            j += 1
            lps[i] = j

            i += 1

        else:
            if j != 0:
                # Since we know that pat[i] != pat[j], we use the assumption that pat[i - k] == pat[j - k] for k = 1...j
                # to skip checking cases we know will already match. Note that this maintains the loop invariant.
                # We move the prefix index to the longest proper prefix of pat[:j-1] which is also a suffix
                # In the next iteration we check if this prefix can be extended
                j = lps[j - 1]

            else:
                # Nothing matches, so we set lps[i] = 0 and increment
                lps[i] = 0
                i += 1