# Wimbledon Momentum Analysis

Code for the **2024 COMAP MCM/ICM Mathematical Contest in Modeling** (Problem C).

**Team:** Aryan Mittal, Joseph Campbell, Ojas Kalra

---

## Overview

This project quantifies and predicts **momentum swings** in professional tennis using point-by-point data from the 2023 Wimbledon tournament. We develop a novel lead metric, define momentum mathematically, and train a machine learning model to predict when momentum shifts are likely to occur.

The full write-up is available in [`final_report.pdf`](./final_report.pdf).

---

## Methodology

**Lead Model (`win_prob.py`)** — We define a player's "lead" at any point in a match as the probability that a replacement-level player, inheriting their current score and serve, would win the match. This is computed recursively from the match state `(sets, games, points, server)` using a constant serve-win probability `p_s = 0.67` (the Wimbledon average).

**Momentum** — Momentum `m(t)` is defined as the derivative of the smoothed lead curve. Raw lead values are first smoothed using Single Exponential Smoothing (`α = 0.2`) to capture trends rather than point-to-point noise.

**Outperformance Analysis** — We validate that momentum is not mere random noise by computing each player's expected points over the next `k` points and comparing to actual outcomes. Players with positive momentum outperformed expectations at over **1.4× the rate** of players without it, with this effect growing stronger in later rounds.

**Swing Prediction (`analysis.ipynb`)** — A Gradient Boosting Classifier (XGBoost) is trained on rounds 3–4 (5,707 points) and tested on rounds 5–7 (1,577 points) to predict momentum swing points. Overall F1 scores of **51–52%** across the test set, rising to **71–73%** on the Medvedev vs. Eubanks Round 5 match.

The three most predictive features (beyond current momentum) are: distance run by each player and serve speed.