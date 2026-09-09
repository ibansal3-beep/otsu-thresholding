import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage.filters import threshold_otsu

from otsu import otsu_threshold, apply_threshold


def load_grayscale_image(path):
    """
    Load an image and convert it to 8-bit grayscale.
    """
    image = Image.open(path).convert("L")
    return np.array(image)


def run_experiment(image_path, output_dir="results"):
    """
    Run the custom Otsu implementation on one image and
    save visualizations and comparison results.
    """

    os.makedirs(output_dir, exist_ok=True)

    image = load_grayscale_image(image_path)

    # Our implementation
    threshold, sigma_b_squared, hist = otsu_threshold(image)
    binary = apply_threshold(image, threshold)

    # Library implementation for verification only
    library_threshold = int(threshold_otsu(image))

    print(f"Image: {image_path}")
    print(f"Our Otsu threshold: {threshold}")
    print(f"scikit-image threshold: {library_threshold}")

    # Save binary result
    Image.fromarray(binary).save(
        os.path.join(output_dir, "binary.png")
    )

    # Plot original image
    plt.figure()
    plt.imshow(image, cmap="gray")
    plt.title("Original Grayscale Image")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, "original.png"),
        dpi=300
    )
    plt.close()

    # Plot histogram
    plt.figure()
    plt.plot(np.arange(256), hist)
    plt.axvline(
        threshold,
        linestyle="--",
        label=f"Otsu threshold = {threshold}"
    )
    plt.xlabel("Gray Level")
    plt.ylabel("Number of Pixels")
    plt.title("Gray-Level Histogram")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, "histogram.png"),
        dpi=300
    )
    plt.close()

    # Plot between-class variance
    plt.figure()
    plt.plot(np.arange(256), sigma_b_squared)
    plt.axvline(
        threshold,
        linestyle="--",
        label=f"Maximum at k = {threshold}"
    )
    plt.xlabel("Threshold k")
    plt.ylabel("Between-Class Variance")
    plt.title("Otsu Criterion")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, "otsu_criterion.png"),
        dpi=300
    )
    plt.close()

    # Plot binary result
    plt.figure()
    plt.imshow(binary, cmap="gray")
    plt.title(f"Otsu Thresholded Image (T = {threshold})")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, "thresholded.png"),
        dpi=300
    )
    plt.close()


if __name__ == "__main__":
    run_experiment("images/test_image.png")
