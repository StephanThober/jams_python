#!/usr/bin/env python
import numpy as np

def sobol_index(s=None, ns=None, ya=None, yb=None, yc=None, si=True, sti=True):
    """
        Calculates the first-order Si and total STi variance-based sensitivity indices
        after Saltelli et al. (2008) with improvements of Saltelli (2002).

        Definition
        ----------
        def sobol_index(s=None, ns=None, ya=None, yb=None, yc=None, si=True, sti=True):


        Optional Input
        --------------
        Either
          s        ns*(k+2) model outputs
          ns      base sample number
        or
          ya       ns model outputs
          yb       second ns model outputs
          yc       (ns,k) model outputs
        with k: # or parameters. See Saltelli et al. (2008, p. 164ff) for definitions.
        si         if True: output Si
        sti        if True: output STi


        Output
        ------
        First-order sensitivity indices Si and Total sensitivity indices STi.


        Restrictions
        ------------
        The right order and size is assumed if s and ns are given.
        If s, ns and ya are given then it is assumed that the use gave ya, yb and yc.


        References
        ----------
        Saltelli, A. (2002). Making best use of model evaluations to compute sensitivity indices.
            Computer Physics Communications, 145(2), 280-297.
        Saltelli, A. et al. (2008). Global sensitivity analysis. The primer.
         John Wiley & Sons Inc., NJ, USA, ISBN 978-0-470-05997-5 (pp. 1-292)


        Examples
        --------
        >>> import numpy as np
        >>> iya = np.array([-257.0921, -152.8434,  -68.7691, -129.8188,  -89.9667])
        >>> iyb = np.array([-174.3796, -147.3429, -119.2169, -102.7477, -160.2185])
        >>> iyc = np.array([[-101.2691, -139.5885, -127.6342, -106.9594, -115.8792], \
                           [-130.0901, -154.8311,  -24.3989, -133.4675, -169.0250], \
                           [-180.9130, -140.7924, -127.3886,  -93.2011, -119.7757], \
                           [-171.2342, -146.7013, -118.9833, -102.5973, -163.5437], \
                           [-255.2163, -179.8984, -131.5042, -103.7205, -167.4869], \
                           [-258.7999, -125.7803, -116.5700, -129.3884, -157.6105], \
                           [-169.9223, -163.9877, -120.3642,  -89.8831, -160.3463], \
                           [-173.9842, -144.7646, -119.3019,  -95.3019, -182.1460], \
                           [-193.2946, -155.0912, -141.4387, -107.3154, -171.4209], \
                           [-174.3416, -147.3517, -119.2144, -102.7560, -160.2369]])
        >>> isi1, isti1 = sobol_index(iya,iyb,iyc)
        >>> print isi1
        [-0.17246466  0.68527704  1.34420855  1.5806421   3.79371374  3.32517435
          1.61709097  1.67219243  2.35600424  1.63096441]
        >>> print isti1
        [ 0.97189473  0.48209728 -0.07413016 -0.56043738 -2.27993476 -1.64234972
         -0.61288843 -0.75492424 -1.31113697 -0.57241965]

        >>> isi2, isti2 = sobol_index(ya=iya,yb=iyb,yc=iyc)
        >>> print isi2
        [-0.17246466  0.68527704  1.34420855  1.5806421   3.79371374  3.32517435
          1.61709097  1.67219243  2.35600424  1.63096441]

        >>> s = np.concatenate((iya, iyb, np.ravel(iyc)))
        >>> ns = np.size(iya)
        >>> isi3, isti3 = sobol_index(s, ns)
        >>> print isi3
        [-0.17246466  0.68527704  1.34420855  1.5806421   3.79371374  3.32517435
          1.61709097  1.67219243  2.35600424  1.63096441]

        >>> isi4, isti4 = sobol_index(s=s, ns=ns)
        >>> print isi4
        [-0.17246466  0.68527704  1.34420855  1.5806421   3.79371374  3.32517435
          1.61709097  1.67219243  2.35600424  1.63096441]

        >>> isi5, = sobol_index(s=s, ns=ns, si=True, sti=False)
        >>> print isi5
        [-0.17246466  0.68527704  1.34420855  1.5806421   3.79371374  3.32517435
          1.61709097  1.67219243  2.35600424  1.63096441]

        >>> isti5, = sobol_index(s=s, ns=ns, si=False, sti=True)
        >>> print isti5
        [ 0.97189473  0.48209728 -0.07413016 -0.56043738 -2.27993476 -1.64234972
         -0.61288843 -0.75492424 -1.31113697 -0.57241965]


        History
        -------
        Written, MC, May 2012
    """
    # Check input
    if (si==False) & (sti==False):
        raise ValueError('No output chosen: si=False and sti=False.')
    # s, ns or ya, yb, yc
    if ((s != None) & (ns != None) & (ya == None)):
        nsa  = ns
        ss   = np.size(s)
        nn   = (ss/nsa)-2
        iyA    = s[0:nsa]
        iyB    = s[nsa:2*nsa]
        iyC    = np.reshape(s[2*nsa:],(nn,nsa))
    else:
        if not (((s != None) & (ns != None) & (ya != None)) | ((ya != None) & (yb !=None) & (yc !=None))):
            raise ValueError('Either s and ns has to be given or ya, yb and yc.')
        if ((s != None) & (ns != None) & (ya != None)):
            iyA     = s
            iyB     = ns
            iyC     = ya
        else:
            iyA     = ya
            iyB     = yb
            iyC     = yc
        nsa = np.size(iyA)
        syc  = np.shape(iyC)
        if not ((nsa == np.size(iyB)) & (nsa == syc[1])):
            raise ValueError('ya and yb must have same size as np.shape(yc)[1].')
        nn = syc[0]
    fnsa  = 1. / np.float(nsa)
    fnsa1 = 1. / np.float(nsa-1)
    #f02   = np.mean(iyA)**2
    f02    = fnsa*np.sum(iyA*iyB)
    iyAiyA = np.mean(iyA**2)
    varA   = iyAiyA - f02
    if si:  isi  = np.empty(nn)
    if sti: isti = np.empty(nn)
    for i in xrange(nn):
        iyCi = iyC[i,:]
        if si:
            iyAiyC = fnsa1*np.sum(iyA*iyCi)
            isi[i] = (iyAiyC - f02) / varA
        if sti:
            iyBiyC  = fnsa1*np.sum(iyB*iyCi)
            isti[i] = 1. - (iyBiyC - f02) / varA

    out = []
    if si:  out = out + [isi]
    if sti: out = out + [isti]
    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # iya = np.array([-257.0921, -152.8434,  -68.7691, -129.8188,  -89.9667])
    # iyb = np.array([-174.3796, -147.3429, -119.2169, -102.7477, -160.2185])
    # iyc = np.array([[-101.2691, -139.5885, -127.6342, -106.9594, -115.8792],
    #                 [-130.0901, -154.8311,  -24.3989, -133.4675, -169.0250],
    #                 [-180.9130, -140.7924, -127.3886,  -93.2011, -119.7757],
    #                 [-171.2342, -146.7013, -118.9833, -102.5973, -163.5437],
    #                 [-255.2163, -179.8984, -131.5042, -103.7205, -167.4869],
    #                 [-258.7999, -125.7803, -116.5700, -129.3884, -157.6105],
    #                 [-169.9223, -163.9877, -120.3642,  -89.8831, -160.3463],
    #                 [-173.9842, -144.7646, -119.3019,  -95.3019, -182.1460],
    #                 [-193.2946, -155.0912, -141.4387, -107.3154, -171.4209],
    #                 [-174.3416, -147.3517, -119.2144, -102.7560, -160.2369]])
    # print np.shape(iya), np.shape(iyb), np.shape(iyc), np.size(iyc)
    # isi1, isti1 = sobol_index(iya,iyb,iyc)
    # print isi1
    # print isti1
    # isi2, isti2 = sobol_index(ya=iya,yb=iyb,yc=iyc)
    # print isi2
    # s = np.concatenate((iya, iyb, np.ravel(iyc)))
    # ns = np.size(iya)
    # print np.shape(s), ns, np.size(s)/ns-2
    # isi3, isti3 = sobol_index(s, ns)
    # print isi3
    # isi4, isti4 = sobol_index(s=s, ns=ns)
    # print isi4
    # isi5, = sobol_index(s=s, ns=ns, si=True, sti=False)
    # print isi5
    # isti5, = sobol_index(s=s, ns=ns, si=False, sti=True)
    # print isti5
