import cv2
from sklearn.cluster import KMeans
import numpy as np
from itertools import compress

class GetDominantColor:

    
    def __init__(self, image, clusters=3):

        self.CLUSTERS = clusters
        #reshaping to a list of pixels
        img=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = img.reshape((image.shape[0] * image.shape[1], 3))

        self.IMAGE = img

        kmeans = KMeans(n_clusters = self.CLUSTERS)
        kmeans.fit(self.IMAGE)
        
        #the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_
        self.LABELS = kmeans.labels_

    
    # 베낌
    # Return a list in order of color that appeared most often.
    def getHistogram(self):
        numLabels = np.arange(0, self.CLUSTERS+1)
        #create frequency count tables

        (hist, _) = np.histogram(self.LABELS, bins = numLabels)
        hist = hist.astype("float")
        hist /= hist.sum()

        colors = self.COLORS
        #descending order sorting as per frequency count
        colors = colors[(-hist).argsort()]
        hist = hist[(-hist).argsort()]
        for i in range(self.CLUSTERS):
            colors[i] = colors[i].astype(int)
        # Blue mask 제거
        fil = [colors[i][2] < 250 and colors[i][0] > 10 for i in range(self.CLUSTERS)]
        colors = list(compress(colors, fil))
        return colors, hist
