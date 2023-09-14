import sys
import copy


def print_interaction(interaction):
    global num_rows
    global num_columns
    (l1, p1), (l2, p2) = interaction
    interactionstring = ["-"] * num_columns
    interactionstring[p1] = "A" if l1 == 0 else "B"
    interactionstring[p2] = "A" if l2 == 0 else "B"
    return_string = ""
    for ele in interactionstring:
        return_string = return_string + ele + " "
    return return_string


if len(sys.argv) < 2:
    exit(0)
arraycode = sys.argv[1]
arrayvalues = arraycode.split("-")
arrayvalues = [int(str) for str in arrayvalues]

num_rows = arrayvalues.pop(0)
num_columns = arrayvalues.pop(0)
partial_array = []
for i in range(num_rows):
    row_code = arrayvalues.pop(0)
    row = [0] * num_columns
    for j in range(num_columns):
        if row_code % 2 == 1:
            row[num_columns - j - 1] = 1
        row_code = row_code // 2
    partial_array.append(row)

## show locating array
print("Input Array")
for row in partial_array:
    row_string = ""
    for element in row:
        if element == 0:
            row_string = row_string + "A "
        else:
            row_string = row_string + "B "
    print(row_string)

#  
interactions_set = []
for p1 in range(num_columns - 1):
    for p2 in range(p1+1, num_columns):
        for l1 in range(2):
            for l2 in range(2):
                interactions_set.append(((l1, p1), (l2, p2)))

# fail-pass outcome
failpass_patterns = {}
for interaction in interactions_set:
    ((l1, p1), (l2, p2)) = interaction
    failpass = [0] * num_rows
    for index, row in enumerate(partial_array):
        if row[p1] == l1 and row[p2] == l2:
            failpass[index] = 1
    failpass_patterns[interaction] = failpass

# check
# チェックまだのインタラクション
exist_list = [True] * len(interactions_set)

# スコア
lostpoint = 0

# no appearance
print("テストされていないもの")
for index, interaction in enumerate(interactions_set):
    count = 0
    for tmp in failpass_patterns[interaction]:
        if tmp == 1:
            count = count + 1
    if count == 0:
        print(print_interaction(interaction))
        exist_list[index] = False
        lostpoint = lostpoint + 1

# 同値類＝限定できないもの
for i in range(len(interactions_set) - 1):
    # interaction still needs to be checked
    if exist_list[i]:
        interaction1 = interactions_set[i]
        # interactions in the equivalent classe
        equivalent_class = []
        equivalent_class.append(interaction1)
        for j in range(i+1, len(interactions_set)):
            # interaction still remain
            if exist_list[j]:
                interaction2 = interactions_set[j]
                is_same = True
                for k in range(num_rows):
                    if failpass_patterns[interaction1][k] != failpass_patterns[interaction2][k]:
                        is_same = False
                        break
                if is_same:
                    exist_list[j] = False
                    equivalent_class.append(interaction2)
        if len(equivalent_class) > 1:
            print("区別できないもの")
            for interaction in equivalent_class:
                print(print_interaction(interaction))
            lostpoint = lostpoint + len(equivalent_class) - 1

# ポイント計算
point = (1 - (lostpoint / len(interactions_set)))*100
print("採点結果: ", int(point), "点")
