# coding: utf-8

import numpy as np

def thin(n_left, n_right, R):
    '''
    Thin lens formula. 
    Returns the dioptric power of a thin lens
    Inputs = left refractive index, right refractive index, radius of curvature (meters).
    /!\ The radius is positive if the lens is convex and negative if the lens is concave.
    For example : both radius of the cornea have positive signs.
    For a biconvex IOL, the anterior radius is positive, and the posterior radius is negative.
    Output is in diopters.
    '''
    power = (n_right - n_left) / R
    return power



def gullstrand(P_left, P_right, thickness, n):
    '''
    Gullstrand formula. 
    Returns the power of the thick lens
    Inputs = dioptric power of left and right surface, thickness of the lens studied (meters), 
    refractive index of the lens studied
    Output is in diopters.
    '''
    power = P_left + P_right - (thickness * P_left * P_right / n)
    return power



def convertSpectaclesToCornea(Spec_ref,d):
    '''
    Converts the refraction measured in the spectacle plane to the corresponding refraction 
    at the corneal plane. Spec_ref = refraction spherical equivalent at spectacle plane (diopters).
    d = vertex distance in meters.
    '''
    K_ref = Spec_ref /(1 - d * Spec_ref)
    return K_ref



def convertCorneaToSpectacles(K_ref,d):
    '''
    Converts the refraction measured in the corneal plane to the corresponding refraction 
    at the spectacle plane. K_ref = refraction spherical equivalent at corneal plane (diopters).
    d = vertex distance in meters.
    '''
    Spec_ref = K_ref /(1 + d * K_ref)
    return Spec_ref



def FFLBFL(n_left, n_right, power):
    '''
    Returns the front focal length and the back focal length of the lens
    Inputs = surrounding refractive indices values, power of the thick lens or lens surfaces.
    '''
    ffl = - n_left / power
    bfl = n_right / power
    return ffl, bfl



def FPPSPP(delta, ffl_thick, ffl_right, bfl_thick, bfl_left):
    '''
    Returns the first principal plane and second principal plane of a thick lens from :
    - lens thickness (named "delta", meters) | NB : If the system studied is composed of two thick lenses, "thickness" must be replaced by the optical distance between the two lenses : 
    optical distance = physical_distance (right surface of the left lens to left surface of the right lens) - left lens second principal plane + right lens first principal plane
    - front focal lengths of the thick lens | if system of two lenses : of the lens system
    - front focal length of the right lens surface | if system of two lenses : of the right thick lens 
    - back focal lengths of the thick lens | if system of two lenses : of the lens system
    - back focal length of the left surface  | if system of two lenses : of the left thick lens 
    '''
    fpp = delta * ffl_thick / ffl_right
    spp = - delta * bfl_thick / bfl_left
    return fpp, spp



def calcTILP(nco, niol, nvit, nair, naq, Rco1, Rco2, eco, Riol1, Riol2, IOLt, SE, AL, d):
    '''
    This function back-calculates the Theoretical Internal Lens Position (TILP) for a given postoperative eye.
    The TILP is the posterior corneal surface to anterior IOL surface distance that allow thick lens equations to exactly output the postoperative refraction.
    All lengths are in meters. 
    Signs respect the cartesian sign convention : distances to the left are negative, distances to the right are positive. 
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
    AL = anatomical axial length 
    d = vertex distance
    '''

    Pco1 = thin(nair, nco, Rco1)
    Pco2 = thin(nco, naq, Rco2)
    Pco = gullstrand(Pco1, Pco2, eco, nco)
    Pco = Pco + (SE / (1 - d * SE))
    Pco1 = (nco*Pco-nco*Pco2) / (nco - Pco2*eco)
    
    ffl_co1, bfl_co1 = FFLBFL(nair, nco, Pco1)
    ffl_co2, bfl_co2 = FFLBFL(nco, naq, Pco2 )
    ffl_co, bfl_co = FFLBFL(nair, naq, Pco)
    fpp_co, spp_co = FPPSPP(eco, ffl_co, ffl_co2, bfl_co, bfl_co1)
    
    Piol1 = thin(naq, niol, Riol1)
    Piol2 = thin(niol, nvit, Riol2)
    ffl_iol1, bfl_iol1 = FFLBFL(naq, niol, Piol1)
    ffl_iol2, bfl_iol2 = FFLBFL(niol, nvit, Piol2)
    Piol = gullstrand(Piol1, Piol2, IOLt, niol)
    ffl_iol, bfl_iol = FFLBFL(naq, nvit, Piol)
    fpp_iol, spp_iol = FPPSPP(IOLt, ffl_iol, ffl_iol2, bfl_iol, bfl_iol1)
    
    Hi_Hprimei = IOLt - fpp_iol + spp_iol
    ALt = AL - (spp_co + eco) - Hi_Hprimei
    
    elem1 = (Pco * (naq-nvit + ALt*Piol) + naq*Piol)
    elem2= 4*naq*Pco*Piol * (Pco*ALt + ALt*Piol-nvit )
    
    if Piol > 0:
        ELPt = (- np.sqrt(elem1*elem1-elem2)+elem1) / (2*Pco*Piol)           
    else :
        ELPt = ( np.sqrt(elem1*elem1-elem2)+elem1) / (2*Pco*Piol)
        
    ALP = ELPt + (spp_co + eco) -  fpp_iol 
    TILP = ALP - eco

    return TILP



def calcSE(nco, niol, nvit, nair, naq, Rco1, Rco2, eco, Riol1, Riol2, IOLt, TILP_pred, AL, d):
    '''
    This function computes the predicted spherical equivalent at the spectacle plane for a given eye and a given TILP. 
    This function is used to calculate the predicted spherical equivalent once the predicted TILP has been computed. 
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
    The mean corneal radius of curvature is the geometric mean of the flat and steep 
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
