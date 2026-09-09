import numpy as np


def otsu_threshold(image):
    """
    Compute Otsu's optimal threshold from scratch.
    """

    hist, _ = np.histogram(
        image.ravel(),
        bins=256,
        range=(0, 256)
    )

    p = hist.astype(np.float64) / image.size
    levels = np.arange(256)

    omega = np.cumsum(p)
    mu = np.cumsum(levels * p)
    mu_T = mu[-1]

    sigma_b_squared = np.zeros(256, dtype=np.float64)

    valid = (omega > 0) & (omega < 1)

    sigma_b_squared[valid] = (
        (mu_T * omega[valid] - mu[valid]) ** 2
        /
        (omega[valid] * (1 - omega[valid]))
    )

    threshold = int(np.argmax(sigma_b_squared))

    # Statistics at optimal threshold
    omega0 = omega[threshold]
    omega1 = 1.0 - omega0

    mu0 = mu[threshold] / omega0
    mu1 = (mu_T - mu[threshold]) / omega1

    # Total variance
    sigma_t_squared = np.sum(
        ((levels - mu_T) ** 2) * p
    )

    # Separability measure eta*
    eta = (
        sigma_b_squared[threshold] / sigma_t_squared
        if sigma_t_squared > 0
        else 0.0
    )

    stats = {
        "threshold": threshold,
        "omega0": omega0,
        "omega1": omega1,
        "mu0": mu0,
        "mu1": mu1,
        "muT": mu_T,
        "sigma_b_squared": sigma_b_squared[threshold],
        "sigma_t_squared": sigma_t_squared,
        "eta": eta,
    }

    return threshold, sigma_b_squared, hist, stats


def apply_threshold(image, threshold):
    return (image > threshold).astype(np.uint8) * 255
