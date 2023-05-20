
def check_noise_and_index_prob(top, index):
    """
    --> detects if cough is present in the voice or not
    :param input_path:
    :return:
    """
    noise = 1
    prob = 0
    for i, d in enumerate(top):
        if index == d[0]:
            noise = i / len(top)
            prob = d[2]
            break
    return noise, prob
