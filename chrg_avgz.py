
import numpy as np
from scipy.integrate import simps

class ChrgAvgZ:
    '''
    All methods are unit independent.
    '''

    def __init__(self, chrg, cell):
        '''
        chrg should be shaped as (nz, ny, nx)
        that is, z-major, x-contiguous
        '''
        self.chrg = chrg
        self.cell = cell
        self.ngridz = self.chrg.shape[0]

    def xyavg(self):
        avgchrg = [np.mean(self.chrg[i,:,:]) for i in range(self.ngridz)]
        avgchrg = np.array(avgchrg)
        return avgchrg

    def zgrid(self):
        zaxis = np.linspace(0., self.cell[2,2], self.ngridz)
        return zaxis

    def xyarea(self):
        xycross = np.cross(self.cell[0], self.cell[1])
        xyarea = np.linalg.norm(xycross)
        return xyarea

    def zatompos(self, atom_coord, epsilon=0.000001):
        '''
        find atomic position of layered slab
        in descending order
        '''
        zatom = list(atom_coord[:,2])
        zatom.sort(reverse=True)
        zatom_dup = [zatom[0]]
        for i in range(1, len(zatom)):
            if abs(zatom[i]-zatom[i-1]) > epsilon:
                zatom_dup.append(zatom[i])
        zatom_dup = np.array(zatom_dup)
        return zatom_dup

    def intgrl_z(self):
        '''
        mainly for check the charge integration
        '''
        xyarea = self.xyarea()
        avgchrg = self.xyavg()
        zaxis = self.zgrid()
        total_valence = xyarea*simps(avgchrg, zaxis)
        return total_valence

