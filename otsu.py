import numpy as np


def otsu_threshold(image):
    """
    Compute Otsu's optimal threshold from scratch.

    Parameters
    ----------
    image : np.ndarray
        2D grayscale image with intensity values in [0, 255].

    Returns
    -------
    threshold : int
        Gray-level threshold that maximizes between-class variance.

    sigma_b_squared : np.ndarray
        Between-class variance for each possible threshold.

    hist : np.ndarray
        256-bin grayscale histogram.
    """

    # Compute grayscale histogram
    hist, _ = np.histogram(
        image.ravel(),
        bins=256,
        range=(0, 256)
    )

    # Normalize histogram:
    # p_i = n_i / N
    p = hist.astype(np.float64) / image.size

    # Gray levels
    levels = np.arange(256)

    # Zeroth-order cumulative moment:
    # omega(k) = sum_{i=0}^k p_i
    omega = np.cumsum(p)

    # First-order cumulative moment:
    # mu(k) = sum_{i=0}^k i * p_i
    mu = np.cumsum(levels * p)

    # Total mean:
    # mu_T = sum i * p_i
    mu_T = mu[-1]

    # Between-class variance
    sigma_b_squared = np.zeros(256, dtype=np.float64)

    # Only use thresholds that create two non-empty classes
    valid = (omega > 0) & (omega < 1)

    sigma_b_squared[valid] = (
        (mu_T * omega[valid] - mu[valid]) ** 2
        /
        (omega[valid] * (1 - omega[valid]))
    )

    # Threshold that maximizes between-class variance
    threshold = int(np.argmax(sigma_b_squared))

    return threshold, sigma_b_squared, hist


def apply_threshold(image, threshold):
    """
    Convert a grayscale image into a binary image using a threshold.
    """
    return (image > threshold).astype(np.uint8) * 255
