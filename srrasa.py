#!/usr/bin/env python
import numpy as np
import pylab as pl

def srrasa(xy,strata=5,n=3,plot=False):
    
    '''        
        PURPOSE:
        Generates stratified random 2D points within a given rectangular area.
        
        DEFINITION:
        def srrasa(xy,strata=5,n=3,plot=True):
        
        INPUT:
        xy        : list of floats (4), list with the x and y coordinates 
                    enclosing the designated rectangle in the form [x1,x2,y1,y2]
        
        PARAMETERS:
        strata    : int, number of strata per axis
        n         : int, number of random points in each strata
        plot      : bool, if True, stratas and points are plotted,
                    otherwise not:
        
        OUTPUT:
        rand_xy   : ndarray (n,2), x and y coordinates of the stratified random
                    points in the given rectangular.
                             
        EXAMPLE:
        # since the result are random numbers no doctest can be performed.
        # Therefor you find only an example calling sequence here:
        rand_xy = srrasa([652219.,652290.,5772970.,5773040.],
                          strata=4, n=3, plot=True)
        ->  gives you within the rectangle of the given coordinates 16 (4**2)
            stratas with 3 random points in each one.
        
        LICENSE:
        This file is part of the UFZ Python library.
    
        The UFZ Python library is free software: you can redistribute it and/or 
        modify it under the terms of the GNU Lesser General Public License as 
        published by the Free Software Foundation, either version 3 of the License,
        or (at your option) any later version.
    
        The UFZ Python library is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
        GNU Lesser General Public License for more details.
    
        You should have received a copy of the GNU Lesser General Public License
        along with The UFZ Python library.  If not,
        see <http://www.gnu.org/licenses/>.
    
        Copyright 2012 Arndt Piayda
    
        HISTORY:
        Written,  AP, Nov 2012
        Modified, MC, Nov 2012 - default plot=False
    '''
    
    # calculate strata steps
    sw = (xy[1]-xy[0])/strata
    sh = (xy[3]-xy[2])/strata
    xsteps = np.arange(xy[0],xy[1]+sw,sw)
    ysteps = np.arange(xy[2],xy[3]+sh,sh)
    
    # make output array
    rand_xy = np.empty((strata**2*n,2))
    
    # throw random points in each strata
    for j in xrange(strata):
        for i in xrange(strata):
            rand_xy[i*n+strata*n*j:(i+1)*n+strata*n*j,0] = (xsteps[i+1] - \
                                                xsteps[i])*np.random.random(n)\
                                                + xsteps[i]
            rand_xy[i*n+strata*n*j:(i+1)*n+strata*n*j,1] = (ysteps[j+1] - \
                                                ysteps[j])*np.random.random(n)\
                                                + ysteps[j]
    
    # plot stratas and random points within
    if plot:
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        mpl.rc('font', size=20)
        mpl.rc('lines', linewidth=2)
        mpl.rc('axes', linewidth=1.5)
        mpl.rc('xtick.major', width=1.5) 
        mpl.rc('ytick.major', width=1.5) 
        mpl.rcParams['lines.markersize']=6
        
        fig = plt.figure('stratified random sampling')
        sub = fig.add_subplot(111, aspect='equal')
        sub.set_xlim(xy[0],xy[1])
        sub.set_ylim(xy[2],xy[3])
        for i in xrange(strata):
            sub.axhline(y=ysteps[i], color=(166/256., 206/256., 227/256.))
            sub.axvline(x=xsteps[i], color=(166/256., 206/256., 227/256.))
        sub.scatter(rand_xy[:,0],rand_xy[:,1],marker='+', s=60,
                    color=( 51/256., 160/256.,  44/256.))
        sub.set_xlabel('X')
        sub.set_ylabel('Y')
        sub.set_title('strata = %i, n = %i' %(strata,n))
        sub.xaxis.set_major_formatter(mpl.ticker.
                                      ScalarFormatter(useOffset=False))
        sub.yaxis.set_major_formatter(mpl.ticker.
                                      ScalarFormatter(useOffset=False))
        fig.autofmt_xdate(rotation=45)
        plt.tight_layout(pad=1, h_pad=0, w_pad=0)
        plt.show()

    return rand_xy



def srrasa_trans(xy,strata=5,n=3,num=3,rl=0.5,silent=True,plot=True):
    
    '''        
        PURPOSE:
        Generates stratified random 2D transects within a given rectangular
        area.
        
        DEFINITION:
        def srrasa(xy,strata=5,n=3,num=3,silent=True,plot=True):
        
        INPUT:
        xy        : list of floats (4), list with the x and y coordinates 
                    enclosing the designated rectangle in the form [x1,x2,y1,y2]
        
        PARAMETERS:
        strata    : int, number of strata per axis
        n         : int, number of random transects in each strata
        num       : int, number of points in each transect
        rl        : float [0. to 1.], relative length of transect with respect
                    to width of stratum
        silent    : bool, if False, runtime diagnostics are printed to the
                    console, otherwise not
        plot      : bool, if True, stratas and points are plotted,
                    otherwise not
        
        OUTPUT:
        rand_xy   : ndarray (n,2), x and y coordinates of the stratified random
                    transect points in the given rectangular.
                             
        EXAMPLE:
        # since the result are random numbers no doctest can be performed.
        # Therefor you find only an example calling sequence here:
        rand_xy = srrasa_trans([652219.,652290.,5772970.,5773040.], strata=4,
                                n=3, num=5, rl=0.5, silent=True, plot=True)
        ->  gives you within the rectangle of the given coordinates 16 (4**2)
            stratas with 3 random transects in each one. Each transect is
            0.5*width_of_strata long and contains 5 points logarithmical
            distributed.
        
        LICENSE:
        This file is part of the UFZ Python library.
    
        The UFZ Python library is free software: you can redistribute it and/or 
        modify it under the terms of the GNU Lesser General Public License as 
        published by the Free Software Foundation, either version 3 of the License,
        or (at your option) any later version.
    
        The UFZ Python library is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
        GNU Lesser General Public License for more details.
    
        You should have received a copy of the GNU Lesser General Public License
        along with The UFZ Python library.  If not,
        see <http://www.gnu.org/licenses/>.
    
        Copyright 2009-2012 Matthias Cuntz
    
        HISTORY:
        Written, Arndt Piayda, Nov 2012

    '''
    
    # calculate strata steps 
    sw = (xy[1]-xy[0])/strata
    sh = (xy[3]-xy[2])/strata
    xsteps = np.arange(xy[0],xy[1]+sw,sw)
    ysteps = np.arange(xy[2],xy[3]+sh,sh)
    tl = sw*rl
    
    # make output array
    rand_xy = np.empty((strata**2*n*num,2))
    
    o = 0
    for j in xrange(strata):
        for i in xrange(strata):
            for k in xrange(n):
                
                goon = True
                it = 0
                while goon:
                    # random seed in strata
                    seedx=(xsteps[i+1]-xsteps[i])*np.random.random(1)+xsteps[i]
                    seedy=(ysteps[j+1]-ysteps[j])*np.random.random(1)+ysteps[j]
                    
                    # make logarithmic transect
                    tx   =np.arange(1,num+1)
                    dis  =np.sort(tl-np.log(tx)/np.max(np.log(tx))*tl)
                    seedx=np.repeat(seedx,num)+dis
                    seedy=np.repeat(seedy,num)
                    
                    # random angle in strata [deg]
                    angle = 360 * np.random.random(1)
                    
                    # rotate transect to random angle               
                    seedx_trans = -(seedy-seedy[0])*np.sin(np.deg2rad(angle))+\
                                   (seedx-seedx[0])*np.cos(np.deg2rad(angle))+\
                                    seedx[0]
                    seedy_trans =  (seedy-seedy[0])*np.cos(np.deg2rad(angle))+\
                                   (seedx-seedx[0])*np.sin(np.deg2rad(angle))+\
                                    seedy[0]
                    
                    # test if transect is in strata
                    if ((seedx_trans>xsteps[i]).all()) &\
                       ((seedx_trans<xsteps[i+1]).all()) &\
                       ((seedy_trans>ysteps[j]).all()) &\
                       ((seedy_trans<ysteps[j+1]).all()):
                        goon = False
                    
                    if not silent:
                        print 'strata= (', i, ',', j, ')', ' it= ', it
                    it += 1

                rand_xy[o:o+num,0] = seedx_trans
                rand_xy[o:o+num,1] = seedy_trans
                o += num
    
    # plot stratas and random transect points within
    if plot:
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        mpl.rc('font', size=20)
        mpl.rc('lines', linewidth=2)
        mpl.rc('axes', linewidth=1.5)
        mpl.rc('xtick.major', width=1.5) 
        mpl.rc('ytick.major', width=1.5) 
        mpl.rcParams['lines.markersize']=6
        
        fig = plt.figure('stratified random transect sampling')
        sub = fig.add_subplot(111, aspect='equal')
        sub.set_xlim(xy[0],xy[1])
        sub.set_ylim(xy[2],xy[3])
        for i in xrange(strata):
            sub.axhline(y=ysteps[i], color=(166/256., 206/256., 227/256.))
            sub.axvline(x=xsteps[i], color=(166/256., 206/256., 227/256.))
        sub.scatter(rand_xy[:,0],rand_xy[:,1],marker='+', s=60,
                    color=( 51/256., 160/256.,  44/256.))
        sub.set_xlabel('X')
        sub.set_ylabel('Y')
        sub.set_title('strata = %i, n = %i, num = %i' %(strata,n,num))
        sub.xaxis.set_major_formatter(mpl.ticker.
                                      ScalarFormatter(useOffset=False))
        sub.yaxis.set_major_formatter(mpl.ticker.
                                      ScalarFormatter(useOffset=False))
        fig.autofmt_xdate(rotation=45)
        plt.tight_layout(pad=1, h_pad=0, w_pad=0)
        plt.show()

    return rand_xy