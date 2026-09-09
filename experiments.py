import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage.filters import threshold_otsu

from otsu import otsu_threshold, apply_threshold


def load_grayscale_image(path):
    image = Image.open(path).convert("L")
    return np.array(image)


def run_experiment(image_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    image = load_grayscale_image(image_path)

    # Our implementation
    threshold, sigma_b_squared, hist = otsu_threshold(image)
    binary = apply_threshold(image, threshold)

    # Library result only for verification
    library_threshold = int(threshold_otsu(image))

    print(f"\nImage: {image_path}")
    print(f"Our Otsu threshold: {threshold}")
    print(f"scikit-image threshold: {library_threshold}")

    # Save binary image
    Image.fromarray(binary).save(
        os.path.join(output_dir, "binary.png")
    )

    # Original
    plt.figure()
    plt.imshow(image, cmap="gray")
    plt.title("Original Image")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, "original.png"),
        dpi=300
    )
    plt.close()

    # Histogram
    plt.figure()
    plt.plot(np.arange(256), hist)
    plt.axvline(
        threshold,
        linestyle="--",
        label=f"Threshold = {threshold}"
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

    # Otsu criterion
    plt.figure()
    plt.plot(np.arange(256), sigma_b_squared)
    plt.axvline(
        threshold,
        linestyle="--",
        label=f"Maximum at k = {threshold}"
    )
    plt.xlabel("Threshold k")
    plt.ylabel("Between-Class Variance")
    plt.title("Otsu Between-Class Variance")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, "criterion.png"),
        dpi=300
    )
    plt.close()

    # Thresholded result
    plt.figure()
    plt.imshow(binary, cmap="gray")
    plt.title(f"Thresholded Image (T = {threshold})")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, "thresholded.png"),
        dpi=300
    )
    plt.close()

    return threshold, library_threshold


if __name__ == "__main__":

    experiments = {
        "fig1_a_character_new_ribbon":
            "images/fig1_a_character_new_ribbon.png",

        "fig1_e_character_old_ribbon":
            "images/fig1_e_character_old_ribbon.png",

        "fig2_a_texture":
            "images/fig2_a_texture.png",

        "fig2_e_texture":
            "images/fig2_e_texture.png",
    }

    for name, image_path in experiments.items():
        run_experiment(
            image_path,
            output_dir=os.path.join("results", name)
        )
