def levenstein_distance(str_1: str, str_2: str) -> int:
    def dist(i, j):
        if i == 0 and j == 0:
            return 0
        elif i == 0 and j > 0:
            return j
        elif j == 0 and i > 0:
            return i
        else:
            m = 0 if str_1[i - 1] == str_2[j - 1] else 1
            return min(dist(i, j - 1) + 1,
                       dist(i - 1, j) + 1,
                       dist(i - 1, j - 1) + m)

    return dist(len(str_1), len(str_2))
