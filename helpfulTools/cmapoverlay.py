import matplotlib.pyplot as plt 
import matplotlib.image as img
location = ("fulloverlayresults.png")
#Creates Color Map of Image measuring brightness values

colormapdata = img.imread(location)
plt.figure(figsize=(16, 9)) 
plt.pcolormesh(colormapdata, cmap = "hot")
plt.colorbar()
plt.savefig(("fulloverlayresultscmap.png"), bbox_inches='tight', pad_inches=0.0, dpi=200,)
plt.close()