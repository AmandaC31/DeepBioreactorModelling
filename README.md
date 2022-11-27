[![Visit the Huggingface Space](https://huggingface.co/front/assets/huggingface_logo-noborder.svg)](https://huggingface.co/spaces)

# Deep-Bioreactor-Modelling

This [app](https://huggingface.co/spaces) allows bioreactor operators to determine their feedstock characteristics from reading only process sensors,
letting them set up their physical models to optimize their process control with ease.
The deep-models were trained on an [ASM1 model implementation](https://github.com/wwtmodels/Activated-Sludge-Models) by 
[Flores-Alsina et al. (2015)](https://doi.org/10.1016/j.watres.2015.07.014) 
that was modified by us to simulate only one aerobic batch bioreactor instead of a full waste-water-management plant.

The models presented here predict the following variables:

1. Readily Biodegradable Substrate (*units*)
2. Slowly Biodegradable Organic Matter Concentration (*units*)
3. Soluble Ammonia Nitrogen Concentration (*units*)
4. Soluble Biodegradable Organic Nitrogen Concentration (*units*)
5. Particulate (slowly) Biodegradable Organic Nitrogen (*units*)

The models use only time-series of the first-day (15 minute intervals) of the following sensor data:

1. Dissolved Oxygen Concentration (*units*)
2. Ammonia-Ion Concentration ($mol/L$)
3. Nitrate-Ion Concentration ($mol/L$)
4. $H^+$-Ion Concentration ($mol/L$ &= $10^{-pH}$)

This work was conducted as part of a Final Design Project for the Bioresource Engineering (B.Eng.) program at McGill University.
For more details on model training and other background information please see the report by [Crèche & Harms (2022)]().