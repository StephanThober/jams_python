#!/usr/bin/env python
import numpy as np                       # array manipulation
import netCDF4 as nc                     # netCDF interphase

def writenetcdf(fhandle, vhandle=None, var=None, time=None, isdim=False, name=None, dims=None,
                attributes=None, fileattributes=None, comp=False, vartype=None):
    """
        Writes dimensions, variables, dependencies and attributes to NetCDF file
        for 1D to 6D data.

        All attribues must be lists; except the data itself.

        Definition
        ----------
        def writenetcdf(fhandle, vhandle=None, var=None, time=None, isdim=False, name=None, dims=None,
                        attributes=None, fileattributes=None, comp=False):


        Input           Format                 Description
        -----           -----                  -----------
        fhandle         string                 file handle of nc.Dataset(FileName, 'w')
        vhandle         string                 variable handle of the particular variable
        var             array like             data (assumed to be netcdf float4)
        time            integer or array like  particular time step of the data
        isdim           boolean                defines if current var is a dimension
        name            string                 name of the variable
        dims            1D list                variable dependencies (e.g. [time, x, y])
        attributes      2D list                variable attributes
        fileattributes  2D list                global attributes of NetCDF file (history, description, ...)
        comp            boolean                compress data on the fly using zlib
        vartype         string                 netcdf variable type
                                               default: 'f4' for normal variables
                                                        'f8' for variable with isdim=True and dims=None (=unlimited)


        Description
        -----------
        Open the NetCDF:
          fhandle =  nc.Dataset("Filename", 'w', format='NETCDF4')

        Then call writenetcdf with specifications of the dimensions:
          define
          - the dimension (isdim=True)
          - attributes of the dimensions (e.g. attributes=['units', 'm'])
          - the data of the dimensions as var=numpy.array or None (=unlimited dimension),

        Now write the data as variables:
        - when creating a variable, save the variable handle (vhandle)
        - specify the dimensions of data with dims
        - specify the timestep or timesteps with time


        Examples
        --------
        >>> import numpy as np
        >>> import netCDF4 as nc
        >>> fhandle =  nc.Dataset('writenetcdf_test.nc', 'w', format='NETCDF4')
        >>> dat    = np.array([[-9., 5., 5., -9. ,5.,-9.,5., -9. ,  5., 5.,  5.], \
                                [ 5.,-9.,-9., -9. ,5.,-9.,5., -9. , -9.,-9.,  5.], \
                                [ 5.,-9.,-9., -9. ,5., 5.,5., -9. ,  5., 5.,  5.], \
                                [ 5.,-9.,-9., -9. ,5.,-9.,5., -9. ,  5.,-9., -9.], \
                                [-9., 5., 5., -9. ,5.,-9.,5., -9. ,  5., 5.,  5.] ])
        >>> FiAtt   = ([['description', 'test writing with writenetcdf.py'], \
                       ['history'    , 'Created by Matthias Zink']])
        >>> handle  = writenetcdf(fhandle, fileattributes=FiAtt)

        # dimensions
        >>> varName = 'time'
        >>> dims    = None
        >>> varAtt  = ([['units',    'hours since 2011-01-01 00:00:00'], \
                        ['calendar', 'gregorian']])
        >>> thand   = writenetcdf(fhandle, name=varName, dims=dims, attributes=varAtt, isdim=True)

        >>> varName = 'lon'
        >>> varAtt  = ([['units'         , 'degrees_east'], \
                        ['standard_name' , 'longitude'   ], \
                        ['missing_value' , -9.]])
        >>> dims    = np.shape(dat)[0]
        >>> var     = np.arange(np.shape(dat)[0])+1
        >>> handle  = writenetcdf(fhandle, name=varName, dims=dims, var=var, attributes=varAtt, isdim=True)

        >>> varName = 'lat'
        >>> varAtt  = ([['units'         , 'degrees_north'], \
                        ['standard_name' , 'latitude'     ], \
                        ['missing_value' , -9.]])
        >>> dims    = np.shape(dat)[1]
        >>> var     = np.arange(np.shape(dat)[1])+1
        >>> handle  = writenetcdf(fhandle, name=varName, dims=dims, var=var, attributes=varAtt, isdim=True)

        # times & variable
        >>> times   = np.array([0.5, 1., 1.5, 2.])
        >>> handle  = writenetcdf(fhandle, thand, time=range(np.size(times)), var=times)

        >>> varName = 'TESTING'
        >>> varAtt  = ([['units'        , 'm'                              ], \
                        ['long_name'     ,'Does this writing routine work?'], \
                        ['missing_value' , -9.]])
        >>> dims    = ['time','lon','lat']
        >>> vhand   = writenetcdf(fhandle, name=varName, dims=dims, attributes=varAtt, comp=True)
        >>> for i in xrange(2): \
                handle  = writenetcdf(fhandle, vhand, time=i, var=dat*(i+1))
        >>> handle  = writenetcdf(fhandle, vhand, time=[2,3], var=np.array([dat*2,dat*3]))

        # type other than float
        >>> varName = 'TESTING2'
        >>> varAtt  = ([['units'        , 'm'                              ], \
                        ['long_name'     ,'Does this writing routine work?'], \
                        ['missing_value' , -9]])
        >>> dims    = ['time','lon','lat']
        >>> typ     = 'i4'
        >>> vhand   = writenetcdf(fhandle, name=varName, dims=dims, attributes=varAtt, comp=True, vartype=typ)
        >>> for i in xrange(2): \
                handle  = writenetcdf(fhandle, vhand, time=i, var=np.array(dat,dtype=np.int)*(i+1))

        # check file
        >>> from readnetcdf import *
        >>> print readnetcdf('writenetcdf_test.nc', variables=True)
        [u'time', u'lon', u'lat', u'TESTING', u'TESTING2']
        >>> readdata = readnetcdf('writenetcdf_test.nc', var='TESTING')
        >>> print np.any((readdata[0,:,:] - dat) != 0.)
        False
        >>> readdata2 = readnetcdf('writenetcdf_test.nc', var='TESTING2')
        >>> print np.any((readdata2[0,:,:] - np.array(dat,dtype=np.int)) != 0.)
        False
        >>> if readdata.dtype == np.dtype('float32'): print 'Toll'
        Toll
        >>> if readdata2.dtype == np.dtype('int32'): print 'Toll'
        Toll

        >>> import os
        >>> os.remove('writenetcdf_test.nc')


        History
        -------
        Written,  MZ/MC, Feb 2012
        Modified, ST,    May 2012 - type 'f8' for time dimension
                  MC,    Jun 2012 - vartype
    """

    # create File attributes
    if fileattributes != None:
        for i in xrange(len(fileattributes)):
            fhandle.setncattr(fileattributes[i][0], fileattributes[i][1])
        return None

    # create dimensions
    if vhandle != None:
        hand = vhandle
    else:
        if vartype == None:
            typ = 'f4'
            if isdim:
                if dims == None:
                    typ = 'f8'
        else:
            typ = vartype
        if isdim:
            idim = fhandle.createDimension(name, dims)
            # create variable for the dimension
            if dims == None:
                hand = fhandle.createVariable(name, typ, (name,))
            else:
                hand = fhandle.createVariable(name, typ, (name,))
        else:
            keys   = fhandle.dimensions.keys()
            for i in xrange(len(dims)):
                if dims[i] not in keys:
                    raise ValueError('Dimension '+str(dims[i])+' not in file dimensions: '+''.join([i+' ' for i in keys]))
            hand = fhandle.createVariable(name, typ, (dims), zlib=comp)

    if attributes != None:
        for i in xrange(len(attributes)):
            hand.setncattr(attributes[i][0], attributes[i][1])

    if var != None:
        shand = hand.shape
        if time != None:
            svar = np.shape(var)
            if np.size(np.shape(time)) == 0:
                if np.size(svar) != (np.size(shand)-1):
                    raise ValueError('Variable and handle dimensions do not agree for variable time: '+str(svar)+' and '+str(shand))
            elif np.size(np.shape(time)) == 1:
                if np.size(svar) != np.size(shand):
                    raise ValueError('Variable and handle dimensions do not agree for variable time vector: '+str(svar)+' and '+str(shand))
            else:
                raise ValueError('Time must be scalar or index vector.')
            if np.size(shand) == 1:
                hand[time] = var
            elif np.size(shand) == 2:
                hand[time,:] = var
            elif np.size(shand) == 3:
                hand[time,:,:] = var
            elif np.size(shand) == 4:
                hand[time,:,:,:] = var
            elif np.size(shand) == 5:
                hand[time,:,:,:,:] = var
            elif np.size(shand) == 6:
                hand[time,:,:,:,:,:] = var
            else:
                raise ValueError('Number of dimensions not supported (>6): '+str(np.size(shand)))
        else:
            if np.size(var) != np.size(hand):
                raise ValueError('Variable and handle elements do not agree: '+str(np.size(var))+' and '+str(np.size(hand)))
            if np.size(shand) == 1:
                hand[:] = var
            elif np.size(shand) == 2:
                hand[:,:] = var
            elif np.size(shand) == 3:
                hand[:,:,:] = var
            elif np.size(shand) == 4:
                hand[:,:,:,:] = var
            elif np.size(shand) == 5:
                hand[:,:,:,:,:] = var
            elif np.size(shand) == 6:
                hand[:,:,:,:,:,:] = var
            else:
                raise ValueError('Number of dimensions not supported (>6): '+str(np.size(shand)))
    return hand

if __name__ == '__main__':
    import doctest
    doctest.testmod()