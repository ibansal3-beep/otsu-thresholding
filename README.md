# Otsu Thresholding 

An implementation of Nobuyuki Otsu's classic 1979 automatic threshold selection method.

This repository reproduces the main idea from:

> N. Otsu, "A Threshold Selection Method from Gray-Level Histograms,"  
> *IEEE Transactions on Systems, Man, and Cybernetics*,  
> vol. SMC-9, no. 1, pp. 62-66, January 1979.

The goal of this project is to understand and implement Otsu's method directly from the mathematical formulation in the original paper rather than relying on an existing implementation.

---

## 1. Overview

Image thresholding separates pixels into different classes using their gray-level intensities.

For binary thresholding, a threshold \(k\) divides the pixels into two classes:

$$
C_0 = [0,1,\ldots,k]
$$

and

$$
C_1 = [k+1,\ldots,L-1]
$$

A simple approach might attempt to find a valley between two peaks in the gray-level histogram.

However, Otsu explains that this can become unreliable when:

- the histogram valley is broad or flat,
- the image contains noise,
- the two histogram peaks have very different heights,
- or a clear valley does not exist.

Instead of searching for a local histogram valley, Otsu defines a global measure of how well the two resulting classes are separated.

The optimal threshold is the threshold that maximizes this class separability.

---

## 2. Otsu's Method

Let

$$
p_i = \frac{n_i}{N}
$$

represent the normalized probability of gray level $i$, where:

- $n_i$ is the number of pixels at gray level $i$,
- $N$ is the total number of pixels.

For a candidate threshold $k$, the cumulative probability is

$$
\omega(k)=\sum_{i=0}^{k}p_i
$$

This is the probability of class $C_0$.

The probability of class $C_1$ is

$$
1-\omega(k)
$$

The first-order cumulative moment is

$$
\mu(k)=\sum_{i=0}^{k} i p_i
$$

The total image mean is

$$
\mu_T=\sum_{i=0}^{L-1} i p_i
$$

Otsu showed that the between-class variance can be calculated efficiently as

$$
\sigma_B^2(k)
=
\frac{
[\mu_T\omega(k)-\mu(k)]^2
}{
\omega(k)[1-\omega(k)]
}
$$

The optimal threshold is therefore

$$
k^*
=
\arg\max_k \sigma_B^2(k)
$$

The implementation tests all valid thresholds and returns the value that maximizes the between-class variance.

---

## 3. Why Between-Class Variance?

Otsu defines the relationship

$$
\sigma_T^2
=
\sigma_W^2+\sigma_B^2
$$

where:

- $\sigma_T^2$ is total gray-level variance,
- $\sigma_W^2$ is within-class variance,
- $\sigma_B^2$ is between-class variance.

Because the total variance is constant for a given image,

$$
\min \sigma_W^2
$$

is equivalent to

$$
\max \sigma_B^2
$$

Therefore, maximizing between-class variance gives the threshold that produces the strongest separation between the two gray-level classes.

---

## 4. Separability Measure

Otsu also defines the separability measure

$$
\eta
=
\frac{\sigma_B^2}{\sigma_T^2}
$$

At the optimal threshold,

$$
\eta^*=\eta(k^*)
$$

The value satisfies

$$
0 \leq \eta^* \leq 1
$$

A larger value indicates stronger separation between the two resulting gray-level classes.

The implementation reports:

- optimal threshold $k^*$,
- $\omega_0$,
- $\omega_1$,
- $\mu_0$,
- $\mu_1$,
- $\mu_T$,
- $\eta^*$.

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

The core implementation is contained in:

```text
otsu.py
```

The method is implemented directly from Otsu's cumulative-moment formulation.

The program:

1. Computes the 256-bin gray-level histogram.
2. Normalizes the histogram to obtain $p_i$.
3. Computes the cumulative probability $\omega(k)$.
4. Computes the cumulative first moment $\mu(k)$.
5. Computes the total mean $\mu_T$.
6. Evaluates $\sigma_B^2(k)$ for all valid thresholds.
7. Selects the threshold that maximizes $\sigma_B^2(k)$.
8. Computes the class statistics and separability measure.
9. Applies the selected threshold to produce a binary image.

The main implementation does **not** use `skimage.filters.threshold_otsu()` to determine the threshold.

---

## 7. Experiments

Four images based on examples from Otsu's original paper were used.

### Figure 1(a)

Character `A` produced using a new typewriter ribbon.

This represents a relatively clean foreground/background thresholding problem.

### Figure 1(e)

Character `A` produced using an older ribbon.

This image provides a noisier version of the first experiment.

### Figure 2(a)

Texture example with a difficult broad/flat histogram valley.

### Figure 2(e)

Texture example with a more difficult histogram distribution that is closer to unimodal.

These examples were selected because the original paper uses them to demonstrate that the method does not depend on identifying a sharp local valley in the histogram.

---

## 8. Experimental Results

The following thresholds were obtained using the implementation in this repository.

| Image | Our Otsu Threshold | scikit-image Threshold | Separability \(\eta^*\) |
|---|---:|---:|---:|
| Fig. 1(a) new ribbon | 157 | 157 | 0.791 |
| Fig. 1(e) old ribbon | 156 | 156 | 0.776 |
| Fig. 2(a) texture | 153 | 153 | 0.857 |
| Fig. 2(e) texture | 142 | 142 | 0.831 |

The independently implemented method produced exactly the same threshold as `scikit-image` for all four experiments.

---

## 9. Detailed Statistics

### Figure 1(a) — New Ribbon

```text
Threshold: 157
omega0: 0.297
omega1: 0.703
mu0: 93.292
mu1: 221.697
muT: 183.521
eta*: 0.791
```

### Figure 1(e) — Old Ribbon

```text
Threshold: 156
omega0: 0.385
omega1: 0.615
mu0: 97.621
mu1: 215.909
muT: 170.366
eta*: 0.776
```

### Figure 2(a) — Texture

```text
Threshold: 153
omega0: 0.532
omega1: 0.468
mu0: 91.060
mu1: 215.366
muT: 149.174
eta*: 0.857
```

### Figure 2(e) — Texture

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

These values should **not** be directly compared numerically with the thresholds obtained in this repository.

The original paper states that the experimental images were represented using different numbers of gray levels. For example:

- Figure 1 used 16 gray levels.
- Figure 2 used 64 gray levels.

The images used in this repository were obtained from reproductions of the figures in the published paper and converted to standard 8-bit grayscale images with values in the range

\[
0 \ldots 255.
\]

Printing, scanning, PDF reproduction, cropping, and grayscale conversion alter the original histogram.

Therefore, reproducing the exact threshold values reported in 1979 is not expected.

The important validation is that the independently implemented algorithm produces exactly the same thresholds as the standard `scikit-image` implementation when both operate on the same input images.

---

## 11. Generated Results

For each image, the experiment script generates:

```text
original.png
binary.png
histogram.png
criterion.png
thresholded.png
```

### Histogram

`histogram.png` displays the gray-level histogram together with the selected threshold.

### Otsu Criterion

`criterion.png` displays the between-class variance

\[
\sigma_B^2(k)
\]

for candidate thresholds.

The selected threshold corresponds to the maximum of this criterion.

### Thresholded Image

`thresholded.png` displays the final binary segmentation produced using the selected threshold.

---

## 12. Running the Project

Clone the repository:

```bash
git clone https://github.com/ibansal3-beep/otsu-thresholding.git
cd otsu-thresholding
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run all experiments:

```bash
python experiments.py
```

The results will be saved inside:

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

`NumPy` is used for histogram calculations and numerical operations.

`Pillow` is used for image loading and saving.

`Matplotlib` is used for visualization.

`scikit-image` is used only as an independent reference implementation for verification.

---

## 14. Use of External Materials

### Otsu's Original Paper

The mathematical implementation in this repository was derived primarily from Nobuyuki Otsu's 1979 paper.

Specifically, the following ideas were taken from the original formulation:

- normalized gray-level histogram \(p_i\),
- division of pixels into classes \(C_0\) and \(C_1\),
- cumulative class probability \(\omega(k)\),
- cumulative first moment \(\mu(k)\),
- total image mean \(\mu_T\),
- within-class, between-class, and total variance,
- the relationship

\[
\sigma_T^2=\sigma_W^2+\sigma_B^2,
\]

- maximization of between-class variance,
- the separability measure \(\eta\),
- and the interpretation of the optimal threshold as the threshold that maximizes class separability.

The code was written independently from these equations rather than copied from an existing Otsu implementation.

### scikit-image Documentation and Implementation

The `scikit-image` documentation and its `threshold_otsu` implementation were studied as a modern reference for the practical use of Otsu thresholding.

Its ideas were used in this project only to:

- understand common modern usage of global Otsu thresholding,
- verify the independently implemented algorithm,
- compare the threshold produced by this implementation with a widely used library implementation.

`skimage.filters.threshold_otsu()` is **not** used to compute the threshold returned by the custom implementation.

It is called separately in `experiments.py` only for validation.

---

## 15. Main Observation

For all four experimental images,

```text
Custom implementation threshold = scikit-image threshold
```

This provides strong evidence that the implementation correctly reproduces the binary Otsu threshold-selection algorithm.

The experiments also demonstrate the main idea of the original paper:

> A useful threshold can be selected by globally maximizing class separability instead of relying on a visible local valley in the gray-level histogram.

---

## 16. Limitations

Otsu thresholding is a global intensity-based method.

Its performance can be limited when:

- foreground and background gray levels overlap strongly,
- illumination varies significantly across the image,
- spatial information is important,
- multiple meaningful classes must be separated,
- the histogram provides weak class separation.

The original paper also discusses extension to multiple thresholds. However, the present implementation focuses on the classic binary two-class formulation.

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
*scikit-image Image Processing in Python documentation*.  
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
