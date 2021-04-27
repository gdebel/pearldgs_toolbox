# pearldgs_toolbox_ajo

This repository hosts the Python functions that were created to develop the formula described in the paper "The PEARL-DGS formula : the development of an open-source machine learning-based thick IOL calculation formula" (Guillaume Debellemanière, Mathieu Dubois, Mathieu Gauvin, Avi Wallerstein, Luis F.Brenner, Radhika Rampat, Alain Saad, Damien Gatinel. *American Journal of Ophthalmology*, 2021). 

The PEARL-DGS thick lens formula toolbox is provided in the pearldgs_toolbox_ajo.py Python module. The formula building process, and functions that are related to this specific paper, are described in the Jupyter Notebook.

## Usage

Signs of the variables used as inputs in the functions (or returned by the functions) respect the cartesian sign convention : distances to the left are negative, and distances to the right are positive. Convex lenses have a positive sign and concave lenses have a negative sign. All distances must be converted to meters before being used as inputs, including the biometric parameters that are usually expressed in mm (corneal radii, axial length...) or in micrometers (central corneal thickness).

The toolbox allows to : 

- compute the power of a thin lens from its radius of curvature (meters) and the refractive indices of the surrounding media : 
```python
from pearldgs_toolbox_ajo import *

thin(n_left, n_right, R) 
power (diopters)
```

- compute the power of a thick lens from the power of each lens surface (diopters), its thickness (meters) and its refractive index  : 
```python
gullstrand(P_left, P_right, thickness, n) returns
```

```python
convertSpectaclesToCornea(Spec_ref,d)
```

```python
convertCorneaToSpectacles(K_ref,d):
```

```python
FFLBFL(n_left, n_right, power)
```

```python
FPPSPP(delta, ffl_thick, ffl_right, bfl_thick, bfl_left)
```

```python
calcTILP(nco, niol, nvit, nair, naq, Rco1, Rco2, eco, Riol1, Riol2, IOLt, SE, AL, d)
```

```python
calcSE(nco, niol, nvit, nair, naq, Rco1, Rco2, eco, Riol1, Riol2, IOLt, TILP_pred, AL, d)
```

```python
calcPRC(R1post, R2post)
```

```python
calcARC(R1, R2)
```

```python
calculateSegmentedAL(AL, LT)
```



## Authors and acknowledgments
parler de la FOR, auteurs, datasets
Cooke, TKY, Hill


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

