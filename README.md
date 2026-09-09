# Otsu Thresholding 

An implementation of Nobuyuki Otsu's classic 1979 automatic threshold selection method.

This repository is based primarily on:

> N. Otsu, "A Threshold Selection Method from Gray-Level Histograms,"  
> *IEEE Transactions on Systems, Man, and Cybernetics*,  
> vol. SMC-9, no. 1, pp. 62-66, January 1979.

The goal of this project is to understand and implement Otsu's method directly from the mathematical ideas in the original paper rather than relying on an existing thresholding function.

---

## 1. Overview

Image thresholding separates pixels into different classes using their gray-level intensities.

For binary thresholding, a threshold `k` divides the gray levels into two classes:

- `C0`: gray levels from the minimum value up to `k`
- `C1`: gray levels above `k`

A simple approach might attempt to locate a valley between two peaks in the gray-level histogram.

However, Otsu explains that this can become unreliable when:

- the histogram valley is broad or flat,
- the image contains noise,
- the two peaks have very different heights,
- or a clear valley does not exist.

Instead of searching for a local valley, Otsu evaluates how well the two resulting classes are separated.

The optimal threshold is the threshold that gives the strongest separation between the two classes.

---

## 2. Core Idea of Otsu's Method

The image histogram is first normalized so that each gray level has a probability based on how many pixels have that intensity.

For every possible threshold `k`, the algorithm computes:

- the probability of class `C0`,
- the probability of class `C1`,
- the mean intensity of class `C0`,
- the mean intensity of class `C1`,
- the total image mean,
- the between-class variance.

The best threshold is the one that maximizes the between-class variance.

In simple terms:

> Otsu chooses the threshold that makes the two resulting gray-level groups as different from each other as possible.

---

## 3. Why Between-Class Variance?

Otsu relates three quantities:

- total variance,
- within-class variance,
- between-class variance.

For a fixed image, the total variance does not change.

This means that minimizing within-class variance is equivalent to maximizing between-class variance.

Therefore, the best threshold is the one that creates:

- compact classes internally,
- strong separation between the classes.

This is the central optimization criterion used in the implementation.

---

## 4. Separability Measure

Otsu also defines a separability measure, commonly written as `eta`.

This value compares the between-class variance with the total variance.

Its value lies between 0 and 1.

Interpretation:

- values near 0 indicate poor class separation,
- values near 1 indicate strong class separation.

The implementation reports:

- optimal threshold,
- class probabilities,
- class means,
- total image mean,
- separability value.

---

## 5. Repository Structure

```text
otsu-thresholding/
│
├── images/
│   ├── fig1_a_character_new_ribbon.png
│   ├── fig1_e_character_old_ribbon.png
│   ├── fig2_a_texture.png
│   └── fig2_e_texture.png
│
├── results/
│   ├── fig1_a_character_new_ribbon/
│   ├── fig1_e_character_old_ribbon/
│   ├── fig2_a_texture/
│   └── fig2_e_texture/
│
├── otsu.py
├── experiments.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 6. Implementation

The main implementation is contained in:

```text
otsu.py
```

The implementation follows the cumulative-moment formulation described in Otsu's paper.

The program:

1. Computes a 256-bin grayscale histogram.
2. Normalizes the histogram.
3. Computes cumulative class probabilities.
4. Computes cumulative first-order moments.
5. Computes the total image mean.
6. Evaluates between-class variance for every valid threshold.
7. Selects the threshold with the maximum between-class variance.
8. Computes class statistics and separability.
9. Produces a binary thresholded image.

The main implementation does not use `skimage.filters.threshold_otsu()` to determine the threshold.

---

## 7. Experiments

Four images based on examples from Otsu's original paper were used.

### Figure 1(a)

Character `A` produced using a new typewriter ribbon.

This is a relatively clean foreground/background example.

### Figure 1(e)

Character `A` produced using an older ribbon.

This is a noisier version of the first example.

### Figure 2(a)

Texture example with a broad and difficult histogram valley.

### Figure 2(e)

Texture example with a more difficult histogram shape that is closer to unimodal.

These examples were chosen because the original paper uses them to demonstrate that Otsu's method does not depend on finding a sharp local valley in the histogram.

---

## 8. Experimental Results

The following results were obtained from the implementation in this repository.

| Image | Our Otsu Threshold | scikit-image Threshold | Separability |
|---|---:|---:|---:|
| Fig. 1(a) new ribbon | 157 | 157 | 0.791 |
| Fig. 1(e) old ribbon | 156 | 156 | 0.776 |
| Fig. 2(a) texture | 153 | 153 | 0.857 |
| Fig. 2(e) texture | 142 | 142 | 0.831 |

The independently implemented method produced exactly the same threshold as `scikit-image` for all four images.

---

## 9. Detailed Statistics

### Figure 1(a) - New Ribbon

```text
Threshold: 157
omega0: 0.297
omega1: 0.703
mu0: 93.292
mu1: 221.697
muT: 183.521
eta*: 0.791
```

### Figure 1(e) - Old Ribbon

```text
Threshold: 156
omega0: 0.385
omega1: 0.615
mu0: 97.621
mu1: 215.909
muT: 170.366
eta*: 0.776
```

### Figure 2(a) - Texture

```text
Threshold: 153
omega0: 0.532
omega1: 0.468
mu0: 91.060
mu1: 215.366
muT: 149.174
eta*: 0.857
```

### Figure 2(e) - Texture

```text
Threshold: 142
omega0: 0.755
omega1: 0.245
mu0: 80.295
mu1: 205.175
muT: 110.879
eta*: 0.831
```

---

## 10. Comparison with the Original Paper

The original paper reports approximately the following thresholds:

| Original Experiment | Threshold Reported by Otsu |
|---|---:|
| Fig. 1(a) | 6 |
| Fig. 1(e) | 6 |
| Fig. 2(a) | 33 |
| Fig. 2(e) | 32 |

These threshold values should not be directly compared with the values obtained in this repository.

The original paper states that:

- Figure 1 used 16 gray levels,
- Figure 2 used 64 gray levels.

The images used in this repository were obtained from reproduced figures in the published paper and then converted to standard 8-bit grayscale images.

As a result, the intensity values were altered by:

- printing,
- scanning,
- PDF reproduction,
- cropping,
- grayscale conversion.

Therefore, reproducing the exact threshold values reported in 1979 is not expected.

The important validation is that the custom implementation and `scikit-image` produce the same threshold when both are applied to the same input image.

---

## 11. Generated Results

For each image, the experiment script creates:

```text
original.png
binary.png
histogram.png
criterion.png
thresholded.png
```

### Histogram

The histogram plot shows the gray-level distribution and the selected threshold.

### Otsu Criterion

The criterion plot shows the between-class variance for all candidate thresholds.

The selected threshold corresponds to the maximum of this curve.

### Thresholded Image

The thresholded image shows the final binary segmentation.

---

## 12. Running the Project

Clone the repository:

```bash
git clone https://github.com/ibansal3-beep/otsu-thresholding.git
cd otsu-thresholding
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the experiments:

```bash
python experiments.py
```

The generated outputs will be saved in:

```text
results/
```

---

## 13. Dependencies

The project uses:

```text
numpy
matplotlib
pillow
scikit-image
```

`NumPy` is used for numerical operations and histogram calculations.

`Pillow` is used for loading and saving images.

`Matplotlib` is used for plots and visualizations.

`scikit-image` is used only for independent verification.

---

## 14. Use of External Materials

### Otsu's Original Paper

The implementation was derived primarily from the original 1979 paper.

The following ideas were taken from the paper:

- normalized gray-level histogram,
- division into two classes,
- cumulative class probabilities,
- cumulative first-order moments,
- class means,
- total image mean,
- within-class variance,
- between-class variance,
- total variance,
- maximization of between-class variance,
- separability measure.

The code was written independently based on these ideas rather than copied from an existing implementation.

### scikit-image

The `scikit-image` documentation and `threshold_otsu` function were studied as a modern implementation reference.

They were used to:

- understand common practical usage of Otsu thresholding,
- verify the correctness of the custom implementation,
- compare the thresholds produced by both methods.

`skimage.filters.threshold_otsu()` is not used to compute the threshold returned by the custom implementation.

It is used only as a separate verification step inside `experiments.py`.

---

## 15. Main Observation

For all four experiments:

```text
Custom implementation threshold = scikit-image threshold
```

This strongly supports that the implementation correctly reproduces the classic binary Otsu threshold-selection method.

The experiments also support the central idea from the original paper:

> A useful threshold can be selected by maximizing global class separability rather than relying on a visible histogram valley.

---

## 16. Limitations

Otsu thresholding is a global intensity-based method.

Its performance can be limited when:

- foreground and background intensities overlap strongly,
- illumination varies across the image,
- spatial information is important,
- multiple meaningful classes are present,
- class separation in the histogram is weak.

The original paper also discusses multithresholding, but this repository focuses on the classic two-class version.

---

## 17. References

### Primary Reference

N. Otsu,  
"A Threshold Selection Method from Gray-Level Histograms,"  
*IEEE Transactions on Systems, Man, and Cybernetics*,  
vol. SMC-9, no. 1, pp. 62-66, January 1979.

### Implementation Reference

scikit-image developers,  
`skimage.filters.threshold_otsu`,  
*scikit-image Documentation*.  
Accessed September 2026.

### Thresholding Guide

scikit-image developers,  
"Thresholding,"  
*scikit-image Examples and Documentation*.  
Accessed September 2026.

---

## 18. Author

**Ishita Bansal**  
Arizona State University
