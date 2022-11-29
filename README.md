[![License: MIT](https://img.shields.io/github/license/AmandaC31/DeepBioreactorModelling)](https://github.com/AmandaC31/DeepBioreactorModelling/blob/master/LICENSE)
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://amandac31-deepbioreactormodelling-appbioreactor-chrvos.streamlit.app/)
[![Model Training Code](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1a1GwUq8NcJ6-5fQmNlKK4jmmCuNsnxM_?usp=sharing)

# Deep-Bioreactor-Modelling

This [app](https://amandac31-deepbioreactormodelling-appbioreactor-chrvos.streamlit.app/) allows bioreactor operators to
determine their feedstock characteristics from reading only process sensors,
letting them set up their physical models to optimize their process control with ease.
The deep-models were trained on data generated using a modified version of the 
[ASM1 model implementation](https://github.com/wwtmodels/Activated-Sludge-Models) by 
[Flores-Alsina et al. (2015)](https://doi.org/10.1016/j.watres.2015.07.014). 
This implementation was modified by us to simulate only one aerobic batch bioreactor 
instead of a full waste-water-management plant.

The models presented here were trained in [Colab](https://colab.research.google.com/drive/1a1GwUq8NcJ6-5fQmNlKK4jmmCuNsnxM_?usp=sharing) 
to predict the following variables:

1. Readily Biodegradable Substrate ( $mg/L$)
2. Slowly Biodegradable Organic Matter Concentration ( $mg/L$)
3. Soluble Ammonia Nitrogen Concentration ( $mg/L$)
4. Soluble Biodegradable Organic Nitrogen Concentration ( $mg/L$)
5. Particulate (slowly) Biodegradable Organic Nitrogen ( $mg/L$)

The models use only time-series of the first-day (15 minute intervals) of the following sensor data:

1. Dissolved Oxygen Concentration ( $mg/L$)
2. Ammonia-Ion Concentration ( $mol/L$)
3. Nitrate-Ion Concentration ( $mol/L$)
4. $H^+$-Ion Concentration ( $mol/L = 10^{-pH}$)

This work was conducted as part of a Final Design Project for the Bioresource Engineering (B.Eng.) program at McGill University.
For more details on model training and other background information please see the report by [Crèche & Harms (2022)]().