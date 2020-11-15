import itertools
import os


def log_error_search(logs_directory, list_of_possible_errors=['Traceback'],
                     allowed_error_list=['Returned False in calulations', 'Example']):
    result = []
    for file in os.listdir(logs_directory):
        error_trace = ''
        with open(logs_directory + '/' + file, 'r+') as a:
            lines = a.readlines()
            start = 0
            end = 0
            flag = False
            for i in range(0, len(lines)):
                for error in list_of_possible_errors:
                    if lines[i].startswith(error):
                        start = i
                        flag = True
                    elif lines[i].startswith('$') and flag is True:
                        end = i
                        flag = False
                    elif 'ERROR' in lines[i]:
                        good_error = False
                        for error in allowed_error_list:
                            if error in lines[i]:
                                good_error = True
                        if not good_error:
                            result.append(lines[i])
            for x in range(start, end):
                error_trace += lines[x] + ' '
            if error_trace not in result:
                result.append(error_trace)
                print('Finished to check logs for errors')
    return result


def remove_none_values(in_dictionary):
    keys_to_remove = []
    for key, value in in_dictionary.items():
        if value is None:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        in_dictionary.pop(key, None)
    return in_dictionary


# Returns variations, is generated from list of variable dictionaries list
def generate_variations(variations):
    variations_list = []
    for l in range(0, len(variations) + 1):
        for subset in itertools.combinations(variations, l):
            variations_list.append(subset)
    return variations_list




