# Segmentation Step

| <img src="https://github.com/lizier/NPMicroplastic/blob/main/pre-processing/data/Sample/31.01/DSC_0925.png" width="150" height="auto"/> | | <img src="https://github.com/lizier/NPMicroplastic/blob/main/segmentation/data/Sample/31.01/DSC_0925.png" width="150" height="auto"/> |


The segmentation process is based on a training stage using Weka. A subset of the images was manually annotated with binary labels, distinguishing between nail polish and background.

This trained model was then applied to all images using the `apply.bsh` script within Fiji.

The training data and related files are stored in the `weka` directory.da etapa de treinamento, dados das imagens e arquivo do treinamento.

