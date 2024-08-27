import numpy as np
from astroquery.vizier import Vizier
from scipy.interpolate import RegularGridInterpolator

claret2019 = "VI/154"
keys = ["logg", "Teff", "[M/H]", "xi", "Met", "Mod", "Filt"]
v = Vizier(catalog=claret2019)
v.ROW_LIMIT = -1


logg = "<=1.5 & >= 0.5"
Teff = "<=4000 & >=3500"
FeH = "<= 0.0 & >= -0.5"

Teff_exact = 3776
logg_exact = 1.05
FeH_exact = -0.15

s1 = f"LD coefficients (Claret 2019) evaluated @ logg={logg_exact}, Teff={Teff_exact}, FeH={FeH_exact}, xi=2, Mod=A, Filt=A, Z=FeH"
print(s1)
print("-" * len(s1))
res = v.query_constraints(
    logg=logg, Vel=2, Teff=Teff, Met="L", Mod="A", Filt="G", Z=FeH
)

res[0].sort(["logg", "Teff", "Z"])
_logg, _Teff, _Z = (
    np.unique(res[0]["logg"]),
    np.unique(res[0]["Teff"]),
    np.unique(res[0]["Z"]),
)
_u = res[0]["u2"]
_u_mesh = _u.reshape((len(_logg), len(_Teff), len(_Z)))
interp = RegularGridInterpolator((_logg, _Teff, _Z), _u_mesh)

print(f"G: {interp([logg_exact, Teff_exact, FeH_exact])[0]}")
