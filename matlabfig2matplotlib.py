import h5py as h5
import numpy as np
import matplotlib.pyplot as plt

##
filename = '/Users/asrich/ownCloud/Documents/apps_and_codes/matlabfig2hdf5/example1.h5'
f = h5.File(filename,'r')

def plotAttrs(p):
    # check if the plot has attrs Title#, XLabel#, YLabel#, UnknownLabel#
    # TODO: still need to treat UnknownLabel, and also the case with multiple labels
    if 'XLabel1' in p.attrs:
        plt.xlabel(p.attrs['XLabel1'])
    if 'YLabel1' in p.attrs:
        plt.ylabel(p.attrs['YLabel1'])
    if 'Title1' in p.attrs:
        plt.title(p.attrs['Title1'])


def dataArgs(d):
    # check if data has attrs LineStyle, Marker, 'Color [r g b]', DisplayName, LineWidth
    args = {}      
    if 'Color [r g b]' in d.attrs:
        args['color'] = d.attrs['Color [r g b]']
    if 'LineStyle' in d.attrs:
        args['linestyle'] = d.attrs['LineStyle']
    if 'Marker' in d.attrs:
        args['marker'] = d.attrs['Marker']
    if 'DisplayName' in d.attrs:
        args['label'] = d.attrs['DisplayName']
    if 'LineWidth' in d.attrs:
        args['linewidth'] = d.attrs['LineWidth']
    return args
    

plots = [f[k] for k in sorted(f.keys()) if k.startswith('Plot')]
plt.clf()
for j,p in enumerate(plots):
    plt.subplot(len(plots),1,j+1)
    
    datatraces = [p[key] for key in p.keys() if key.startswith('Data')]
    for d in datatraces:
        if 'XData' in d:
            if 'LData' in d:
                # TODO: need to test this code
                # should be a plot with errorbars
                yerr = np.array([d['LData'], d['UData']])
                x = d['XData']
                y = d['YData']
                args = plotArgs(d)
                plt.errorbar(x,y,yerr,**args)
            elif 'ZData' in d:
                # should be a 3D scatter plot (or 3D quiver?)
                # TODO: implement this case
                pass
            elif 'VData' in d:
                # should be a quiver plot
                # TODO: implement this case
                pass
            else:
                # regular 2D scatter/line plot
                # should have 'XData', 'YData', need to check
                x = d['XData']
                y = d['YData']                
                args = plotArgs(d)
                plt.plot(x,y,**args)

        elif 'FaceCoords' in d:
            print('Plotting of FaceCoords data is not yet implemented')
            # TODO: implement this case
        else:
            print('No data found for plotting')

    plotAttrs(p)
    
    plt.legend()
    plt.draw()
    plt.show()
                
