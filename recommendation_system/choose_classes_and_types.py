import json


def ChooseClassesAndTypes(interest):
    classes = list(interest.get('classes').items())
    types = list(interest.get('types').items())
    classes = [pair for pair in classes if pair[1] != 0]
    types = [pair for pair in types if pair[1] != 0]

    classes_names = [pair[0] for pair in classes]
    types_names = [pair[0] for pair in types]

    sum_classes = sum([pair[1] for pair in classes])
    sum_types = sum([pair[1] for pair in types])
    proportions_classes = [round(float(pair[1])/sum_classes, 3) for pair in classes]
    proportions_types = [round(float(pair[1])/sum_types, 3) for pair in types]

    num_of_events = 10
    num_classes = [round(num_of_events * n) for n in proportions_classes]
    pairs = []
    nums = []
    for i in range(len(classes)):
        for j in range(len(types)):
            num = round(num_classes[i] * proportions_types[j])
            if num != 0:
                pairs.append((classes_names[i], types_names[j]))
                nums.append(num)

    while sum(nums) != num_of_events:
        diff = sum(nums) - num_of_events
        if diff < 0:
            max = 0
            max_i = 0
            for i in range(len(nums)):
                if nums[i] > max:
                    max = nums[i]
                    max_i = i
            nums[max_i] = max + abs(diff)
        elif diff > 0:
            min = 10
            min_i = 0
            for i in range(len(nums)):
                if nums[i] < min:
                    min = nums[i]
                    min_i = i
            if min - abs(diff) >= 0:
                nums[min_i] = min - abs(diff)
    classes_and_types = [(item[0], item[1]) for item in zip(pairs, nums) if item[1] != 0]

    classes_names = list(set([item[0][0] for item in classes_and_types]))
    for_dict = []
    for i in range(len(classes_names)):
        class_name = classes_names[i]
        types_num = [(item[0][1], item[1]) for item in classes_and_types if item[0][0] == class_name]
        types_num = dict(types_num)
        for_dict.append((class_name, types_num))
    dict_res = dict(for_dict)

    return json.dumps(dict_res)
