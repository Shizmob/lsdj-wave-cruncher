def estimate_pitch(samples, rate=44100, threshold=0.1):
    """ Given a number of samples, try to estimate the pitch using the YIN algorithm. Returns (pitch, probability) tuple. """
    n = len(samples)
    h = n // 2
    estimate = 0
    probability = 0.0
    diff = [0.0] * h

    # Calculate squared correlation between samples.
    for i in range(1, h):
        for j in range(h):
            d = samples[j] - samples[j + i]
            diff[i] += d * d
        if i % 1000 == 0:
            print(i, h)
    
    # Calculate cumulative mean.
    mean = [0.0] * h
    mean[0] = 1.0

    sum = 0.0
    for i in range(1, h):
        sum += diff[i]
        mean[i] = diff[i] * i / sum

    # Search for over-threshold values to find tau.
    tau = 2
    while tau < h:
        if mean[tau] >= threshold:
            tau += 1
            continue
        while tau + 1 < h and mean[tau + 1] < mean[tau]:
            tau += 1

        probability = 1 - mean[tau]
        break
    
    if tau == h or mean[tau] >= threshold:
        return (-1, 0.0)
    
    # Parabolically interpolate in order to improve estimate.
    if tau < 1:
        if mean[tau] > mean[tau + 1]:
            tau += 1
    elif tau + 1 >= h:
        if mean[tau] > mean[tau - 1]:
            tau -= 1
    else:
        tau += (mean[tau + 1] - mean[tau - 1]) / (2 * (2 * mean[tau] - mean[tau + 1] - mean[tau - 1]))
    
    return (rate / tau, probability)
