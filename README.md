# pearldgs_toolbox_ajo

This repository hosts the Python functions that were created to develop the formula described in the paper "The PEARL-DGS formula : the development of an open-source machine learning-based thick IOL calculation formula" (Guillaume Debellemanière, Mathieu Dubois, Mathieu Gauvin, Avi Wallerstein, Luis F.Brenner, Radhika Rampat, Alain Saad, Damien Gatinel. *American Journal of Ophthalmology*, 2021). 

The PEARL-DGS thick lens formula toolbox is provided in the pearldgs_toolbox_ajo.py Python module. The formula building process, and functions that are related to this specific paper, are described in the Jupyter Notebook.

## Usage

Signs of the variables used as inputs in the functions (or returned by the functions) respect the cartesian sign convention : distances to the left are negative, and distances to the right are positive. Convex lenses have a positive sign and concave lenses have a negative sign. 

The toolbox allows to : 

- compute the power of a thin lens from its radius of curvature and the refractive indices of the surrounding media : 

```python
pearldgs_toolbox_ajo.thin(n_left, n_right, R) # returns 'power (D)'
```

## Authors and acknowledgments
parler de la FOR, auteurs, datasets
Cooke, TKY, Hill


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

