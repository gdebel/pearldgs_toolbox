# coding: utf-8

import numpy as np

def thin(n_left, n_right, R):
    '''
    Thin lens formula. 
    Returns the dioptric power of a thin lens
    Inputs = radius of curvature, left and right refractive indices.
    /!\ The radius is positive if the lens is convex and negative if the lens is concave.
    For example : both radius of the cornea have positive signs.
    For a biconvex IOL, the anterior radius is positive, and the posterior radius is negative.
    R = in meters
    '''
    power = (n_right - n_left) / R
    return power



def gullstrand(P_left, P_right, thickness, n):
    '''
    Gullstrand formula. 
    Returns the power of the thick lens
    Inputs = dioptric power of each surface, thickness of the lens studied (meters), 
    refractive index of the lens studied
    '''
    power = P_left + P_right - (thickness * P_left * P_right / n)
    return power



def convertSpectaclesToCornea(Spec_ref,d):
    '''
    Converts the refraction measured in the spectacle plane to the corresponding refraction 
    in the corneal plane. d = vertex distance in meters. SE = diopters.
    '''
    K_ref = Spec_ref /(1 - d * Spec_ref)
    return K_ref



def convertCorneaToSpectacles(K_ref,d):
    '''
    Converts the refraction measured in the spectacle plane to the corresponding refraction 
    in the corneal plane. d = vertex distance in meters. SE = diopters.
    '''
    Spec_ref = K_ref /(1 + d * K_ref)
    return Spec_ref



def FFLBFL(n_left, n_right, power):
    '''
    Returns the front focal length and the back focal length of the lens
    Inputs = power of the lens and surrounding refractive indices values
    '''
    ffl = - n_left / power
    bfl = n_right / power
    return ffl, bfl



def FPPSPP(delta, ffl_thick, ffl_right, bfl_thick, bfl_left):
    '''
    Returns the first principale plane and second principale planes of a thick lens from :
    - lens thickness (if the system studied is composed of two thick lenses, "thickness" must be replaced
    by the optical distance between the two lenses : 
    optical distance = physical_distance - left lens 2d principale plane + right lens first principale plane)
    - front and back focal planes of the thick lens
    - front focal plane of the right surface (or lens if the system studied is composed of two thick lenses)
    - back focal plane of the left surface (or lens if the system studied is composed of two thick lenses)
    '''
    fpp = delta * ffl_thick / ffl_right
    spp = - delta * bfl_thick / bfl_left
    return fpp, spp



def calcTILP(nco, niol, nvit, nair, naq, Rco1, Rco2, eco, Riol1, Riol2, IOLt, SE, AL, d):
    '''
    This function back-calculates the reference TILP (distance between the posterior corneal surface and the 
    anterior lens surface) from the radius of curvatures, thicknesses and indices of the different 
    elements of the post-operative eye, and the postop refraction.
    The reference TILP is the TILP value that enables the optical formula to exactly output the postop refraction. 
    The TILP is then converted to TILP_haptics by adding half of the IOL thickness.
    All lengths are in meters. 
    Signs respect the cartesian sign convention : distances to the left are negative, 
    and distances to the right are positive. 
    nco = refractive index of the cornea
    niol = refractive index of the iol
    nvit =  refractive index of the vitreous
    nair = refractive index of the air
    naq = refractive index of the acqueous
    Rco1 = anterior corneal radius of curvature
    Rco2 = posterior corneal radius of curvature
    eco = corneal thickness
    Riol1 = anterior IOL radius of curvature
    Riol2 = posterior IOL radius of curvature
    IOLt = IOL thickness
    SE = real postoperative SE, spectacle plane
    AL = axial length 
    d = vertex distance
    '''
    
    SEc = convertSpectaclesToCornea(SE,d)
    Pco1 = thin(nair, nco, Rco1)
    Pco2 = thin(nco, naq, Rco2)
    # The real corneal power is calculated
    Pco = gullstrand(Pco1, Pco2, eco, nco)  
    # The corneal power is corrected using the refraction (at corneal plane)
    Pco += SEc
    # The anterior corneal radius of curvature achieving the corrected corneal power is calculated
    Pco1 = (nco*Pco-nco*Pco2) / (nco - Pco2*eco)
    # FFL and BFL are calculated for posterior corneal radius and corrected anterior radius
    ffl_co1, bfl_co1 = FFLBFL(nair, nco, Pco1)
    ffl_co2, bfl_co2 = FFLBFL(nco, naq, Pco2 )
    # FFL, BFL, FPP and SPP are calculated for the entire corrected cornea
    ffl_co, bfl_co = FFLBFL(nair, naq, Pco)
    fpp_co, spp_co = FPPSPP(eco, ffl_co, ffl_co2, bfl_co, bfl_co1)
    # Same calculations for the IOL 
    Piol1 = thin(naq, niol, Riol1)
    Piol2 = thin(niol, nvit, Riol2)
    ffl_iol1, bfl_iol1 = FFLBFL(naq, niol, Piol1)
    ffl_iol2, bfl_iol2 = FFLBFL(niol, nvit, Piol2)
    Piol = gullstrand(Piol1, Piol2, IOLt, niol)
    ffl_iol, bfl_iol = FFLBFL(naq, nvit, Piol)
    fpp_iol, spp_iol = FPPSPP(IOLt, ffl_iol, ffl_iol2, bfl_iol, bfl_iol1)
    # Optical TILP back-calculation :
    ALmod = AL-eco+fpp_iol-spp_co-IOLt-spp_iol
    D1 = ((nvit*naq)/bfl_co)-(naq*Pco)-(naq*Piol)-Pco*Piol*ALmod
    D1square = D1**2
    D2 = 4*Pco*Piol*(ALmod * (naq*Pco + naq*Piol) - nvit*naq)
    D = D1square-D2
    TILP = (-D1 - np.sqrt(D))/(2*Pco*Piol) +spp_co-fpp_iol
    
    return TILP



def calcSE(nco, niol, nvit, nair, naq, Rco1, Rco2, eco, Riol1, Riol2, IOLt, TILP_pred, AL, d):
    '''
    This function calculates the postoperative SE at the spectacle plane from the radius of curvatures, 
    thicknesses and indices of the different elements of the eye, for a given TILP value. 
    The TILP value taken as input is the predicted TILP_haptics value, which is converted to the predicted TILP 
    value (distance between the posterior corneal surface and the anterior lens surface)
    All lengths are in meters. 
    Signs respect the cartesian sign convention : distances to the left are negative, 
    and distances to the right are positive. 
    nco = refractive index of the cornea
    niol = refractive index of the iol
    nvit =  refractive index of the vitreous
    nair = refractive index of the air
    naq = refractive index of the acqueous
    Rco1 = anterior corneal radius of curvature
    Rco2 = posterior corneal radius of curvature
    eco = corneal thickness
    Riol1 = anterior IOL radius of curvature
    Riol2 = posterior IOL radius of curvature
    IOLt = IOL thickness
    TILP_haptics = predicted TILP_haptics value
    AL = axial length 
    d = vertex distance
    '''

    # FFL, BFL, FPP, SPP and power calculations for the IOL
    Piol1 = thin(naq, niol, Riol1)
    Piol2 = thin(niol, nvit, Riol2)
    ffl_iol1, bfl_iol1 = FFLBFL(naq, niol, Piol1)
    ffl_iol2, bfl_iol2 = FFLBFL(niol, nvit, Piol2)
    Piol = gullstrand(Piol1, Piol2, IOLt, niol)
    ffl_iol, bfl_iol = FFLBFL(naq, nvit, Piol)
    fpp_iol, spp_iol = FPPSPP(IOLt, ffl_iol, ffl_iol2, bfl_iol, bfl_iol1)
    # posterior corneal power calculation from the predicted posterior corneal radius
    Pco2 = thin(nco, naq, Rco2)
    # "Perfect" anterior corneal radius back-calculation : ARC yielding the desired refractive target 
    # given the predicted TILP
    N = (AL - eco - TILP_pred - IOLt - spp_iol) / nvit
    numk = naq*nco - Pco2*nco * (TILP_pred+fpp_iol- (N*naq)/(N*Piol-1))
    denumk = (nco - eco*Pco2) * (TILP_pred + fpp_iol - (N*naq)/(N*Piol-1)) + naq*eco
    Pco1_mod = numk / denumk
    # The "Perfect" corneal power is calculated
    Pco_mod = Pco1_mod + Pco2 - (eco * Pco1_mod * Pco2 / nco)
    # The real anterior corneal power is calculated
    Pco1 = thin(nair, nco, Rco1)
    # The real total corneal power is calculated
    Pco = gullstrand(Pco1, Pco2, eco, nco) 
    # The predicted refraction at the corneal plane is calculated by subtracting Pco from Pco_mod
    pred_SE_cornea = Pco_mod - Pco
    # The predicted refraction at the spectacle plane is calculated
    pred_SE = convertCorneaToSpectacles(pred_SE_cornea, d)
    return pred_SE



def calcPRC(R1post, R2post):
    '''
    This function should be used instead of the posterior corneal surface prediction function, if the formula
    being developed is based on measured posterior corneal radius data.
    '''
    PRC = np.sqrt(R1post*R2post)
    return PRC



def calcARC(R1, R2):
    '''
    The mean corneal radius of curvature is calculated from the geometric mean of the flat and steep 
    corneal radius of curvatures.
    '''
    ARC = np.sqrt(R1*R2)
    return ARC



def calculateSegmentedAL(AL, LT):
    '''
    CMAL calculation according to Cooke and Cooke (Cooke, D. L. & Cooke, T. L.  :
    Approximating sum-of-segments axial length from a traditional optical low-coherence 
    reflectometry measurement. Journal of Cataract & Refractive Surgery vol. 45 351–354 (2019))
    All distances are in meters.
    '''
    CMAL = 1.23853 + 958.55 * AL - 54.67 * LT
    CMAL = CMAL / 1000
    CMAL += 200/1000000
    return CMAL



def predPRC(ARC):
    '''
    This function developped from Pentacam data predicts the posterior corneal radius of curvature 
    from the anterior radius of curvature. It is used instead of the keratometric index. 
    '''
    if ARC > 0.00697:
        PRC = 0.906499 * ARC - 0.000609
    else:
        PRC = 1.456596 * ARC - 0.004439
    return PRC
