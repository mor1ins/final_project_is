import ast


def сombine(d1, d2):
    united = set(d2.keys()).union(set(d1.keys()))
    result = dict.fromkeys(united, 0)
    for i in d1.keys():
        for j in d2.keys():
            if str(i) == '' and str(i) == str(j):
                result[i] += d1[i] * d2[j]
            else:
                if str(i) == '':
                    result[j] += d1[i] * d2[j]
                if str(j) == '':
                    result[i] += d1[i] * d2[j]
                if str(j) != '' and str(i) != '':
                    st1 = set(str(i)).intersection(set(str(j)))
                    for k in result.keys():
                        if len(st1) != 0 and (st1 == set(k)):
                            result[k] += d1[i] * d2[j]
                            break
    for i in result.keys():
        result[i] = round(result[i], 4)
    f = sum(list(result.values()))
    f = round(f, 4)
    for i in result.keys():
        result[i] = round(result[i] / f, 4)
    return result


def get_masses(_lines):
    masses = {}
    previous_line = ast.literal_eval(_lines[0])
    for line in range(1, len(_lines)):
        current_line = ast.literal_eval(_lines[line])
        masses = сombine(previous_line, current_line)
        previous_line = masses
    return masses.copy()


def get_beliefs(_masses):
    belief = _masses.copy()
    for i in belief.keys():
        for j in belief.keys():
            if i != j:
                if set(str(i)).issuperset(
                        set(str(j))) and i != '' and j != '':
                    belief[i] += _masses[j]
    for i in belief.keys():
        belief[i] = round(belief[i], 4)
    return belief


def get_plses(masses):
    pls = masses.copy()

    for i in pls.keys():
        pls[i] = 0  # init elements with 0
    for i in pls.keys():
        for j in pls.keys():
            if len(set(str(i)).intersection(
                    set(str(j)))) != 0 and i != '':  # if intersection of i and j is not None and i is not ''
                pls[i] += masses[j]  # add mass of j to plausibilities of i
            if j == '':
                pls[i] += masses[j]  # if j is '', add its mass to i

    for i in pls.keys():
        pls[i] = round(pls[i], 4)  # round 4 digits
    return pls


def calc_dempster_shefer(_lines):
    return get_plses(get_masses(_lines)) if len(_lines) > 1 else []


if __name__ == '__main__':
    pathToFile = 'reviews.txt'
    lines = open(pathToFile).readlines()

    print("Intervals")
    print(calc_dempster_shefer(lines))
