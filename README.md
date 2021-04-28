# pearldgs_toolbox_ajo

This repository hosts the Python functions that were created to develop the formula described in the paper "The PEARL-DGS formula : the development of an open-source machine learning-based thick IOL calculation formula" (Guillaume Debellemanière, Mathieu Dubois, Mathieu Gauvin, Avi Wallerstein, Luis F.Brenner, Radhika Rampat, Alain Saad, Damien Gatinel. *American Journal of Ophthalmology*, 2021). Calculations related to the calculation of the theoretical effective lens position are also explained in the following article : "Determining the Theoretical Effective Lens Position of Thick Intraocular Lenses for Machine Learning–Based IOL Power Calculation and Simulation" (Damien Gatinel, Guillaume Debellemanière, Alain Saad, Mathieu Dubois, Radhika Rampat. *Translational Vision Science & Technology*, 2021).

The PEARL-DGS thick lens formula toolbox is provided in the pearldgs_toolbox_ajo.py Python module. The formula building process, and functions that are related to this specific paper, are described in the Jupyter Notebook.

This work is released under the open-source MIT license. Please cite the authors if you use this code in your work.

## Usage

Signs of the variables used as inputs in the functions (or returned by the functions) respect the cartesian sign convention : distances to the left are negative, and distances to the right are positive. Convex lenses have a positive sign and concave lenses have a negative sign. All distances must be converted to meters before being used as inputs, including the biometric parameters that are usually expressed in mm (corneal radii, axial length...) or in micrometers (central corneal thickness).

The toolbox allows to : 

- Compute the power of a thin lens : inputs = radius of curvature (meters) and refractive indices of the surrounding media.
```python
from pearldgs_toolbox_ajo import *

thin(n_left, n_right, R)  # returns thin lens power (diopters)
```

- Compute the power of a thick lens : inputs = power of each lens surface (diopters), lens thickness (meters) and lens refractive index.
```python
gullstrand(P_left, P_right, thickness, n) # returns thick lens power (diopters)
```

- Convert the refraction measured in the spectacle plane to the corresponding refraction in the corneal plane : inputs = refraction at the spectacle plane (diopters) and vertex distance (meters).
```python
convertSpectaclesToCornea(Spectacle_ref,d) # returns the spherical equivalent of the refraction at the corneal plane (diopters)
```

- Convert the refraction measured in the corneal plane to the corresponding refraction in the spectacle plane : inputs = refraction at the corneal plane (diopters) and vertex distance (meters).
```python
convertCorneaToSpectacles(Corneal_ref,d) # returns the spherical equivalent of the refraction at the spectacle plane (diopters)
```

- Compute the front focal length and the back focal length of a lens from the power of the lens and surrounding refractive indices values. The front focal length of a thick lens is expressed from its first principal plane and the back focal length of a thick lens is expressed from its second principal plane. Inputs : surrounding refractive indices and lens power.
```python
FFLBFL(n_left, n_right, power) # returns the front focal length and the back focal length of the lens. 
```

- Compute the first principal plane and the second principal plane of a thick lens. Inputs : lens thickness (delta), front focal length of the thick lens, front focal length of the right surface, back focal length of the thick lens, back focal length of the left surface.
NB : to compute the first and second principal planes of a system of two thick lenses, delta must be equal to the optical distance between the two thick lenses : optical distance = physical distance - left thick lens back focal length + right thick lens back focal length. 
```python
FPPSPP(delta, ffl_thick, ffl_right, bfl_thick, bfl_left) # returns the first principal plane and the second principal plane of the thick lens | lens system.
```

- Compute the Theoretical Internal Lens Position (TILP) for a given postoperative eye. This is the distance from the posterior corneal surface to the anterior IOL surface that leads to the real postoperative spherical equivalent when used in thick lens equations along with the other optical parameters of the eye (cornea and IOL thicknesses, refractive indices and radii of curvature ; refractive index of the acqueous and vitreous ; axial length). This function is used to calculate the target value that will be used as a reference to train the TILP predictive algorithms, using the eyes of the training set. This value can be compared as the thick lens version of the "d" value of the Haigis formula. Inputs : refractive indices of the cornea, IOL, vitreous, air and acqeuous ;  anterior and posterior corneal radii ; corneal thickness ; anterior and posterior IOL radii ; IOL thickness ; postoperative spherical equivalent ; axial length ; vertex distance.
```python
calcTILP(nco, niol, nvit, nair, naq, Rco1, Rco2, eco, Riol1, Riol2, IOLt, SE, AL, d) # returns the TILP (meters).
```
- Compute the predicted spherical equivalent at the spectacle plane for a given eye and a given TILP. This function is used to calculate the predicted spherical equivalent once the predicted TILP has been computed. Inputs : refractive indices of the cornea, IOL, vitreous, air and acqeuous ;  anterior and posterior corneal radii ; corneal thickness ; anterior and posterior IOL radii ; IOL thickness ; predicted TILP ; axial length ; vertex distance.
```python
calcSE(nco, niol, nvit, nair, naq, Rco1, Rco2, eco, Riol1, Riol2, IOLt, TILP_pred, AL, d) # returns the spherical equivalent (diopters).
```

- Calculate the corneal anterior radius of curvature from the steep and flat anterior corneal radii (geometric mean). 
```python
calcARC(R1, R2) # returns ARC (meters)
```

- Calculate the corneal posterior radius of curvature from the steep and flat posterior corneal radii, when available (geometric mean). 
```python
calcPRC(R1post, R2post) # returns PRC (meters)
```

- Calculate the Cooke-modified AL, that approximates the sum-of-segments AL (Cooke D. L. & Cooke T. L.  : Approximating sum-of-segments axial length from a traditional optical low-coherence reflectometry measurement. *Journal of Cataract & Refractive Surgery* vol. 45 351–354 (2019))
```python
calculateSegmentedAL(AL, LT) # returns CMAL (meters)
```


## Authors and acknowledgments
The Postoperative spherical Equivalent Prediction using ARtificial Intelligence and Linear algorithms (PEARL) project aims to assess the potential of Artificial Intelligence (AI) techniques in the IOL calculation field, to determine the optimal architecture of those formulas, and to encourage open research in this field by publishing the experiments and the related code under an open-source license.

It is conducted by Dr Debellemanière, Gatinel and Saad from the Anterior Segment and Refractive Surgery Department at Rothschild Foundation Hospital, Paris. 

The authors thank Dr Ronald Melles (Kaiser Permanente Redwood City Medical Center, Redwood City, California, USA), Dr David Cooke (Great Lakes Eye Care, St. Joseph, Michigan, USA) and Dr Tun Kuan Yeo (Tan Tock Seng Hospital, Singapore) for their thrilling discussions about IOL calculation formulas.


## Contributing
Comments, corrections and suggestions are welcome. Please open an issue first to discuss what you would like to update.

## License
[MIT](https://choosealicense.com/licenses/mit/)

