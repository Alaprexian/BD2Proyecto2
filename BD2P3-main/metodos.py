import random,os,math,cv2,time, rtree, pickle, heapq,json,time, heapq, hashlib
from rtree.index import Index
from scipy.spatial import KDTree
import numpy as np

class Sequential:
    def __init__(self, histograms):
        """
        Inicializa la clase con los histogramas de palabras visuales.
        
        Args:
            histograms (dict): Diccionario con histogramas para cada clase.
        """
        self.lista_valores = []
        for label, hist_list in histograms.items():
            for hist in hist_list:
                self.lista_valores.append((label, hist))
    
    def knnSequential(self, query_hist, k):
        heap = []
        for label, hist in self.lista_valores:
            distancia = np.linalg.norm(hist - query_hist)
            heapq.heappush(heap, (distancia, label))
            if len(heap) > k:
                heapq.heappop(heap)
        return heap
    
    def rangeSearch(self, query_hist, r):
        result = []
        for label, hist in self.lista_valores:
            distancia = np.linalg.norm(hist - query_hist)
            if distancia <= r:
                result.append((distancia, label))
        return result

class RtreeIndex:
    def __init__(self):
        self.ind = None
        self.searchResults = []
    
    def buildRindex(self, histograms):
        if os.path.exists("histograms.data"):
            os.remove("histograms.data")
        if os.path.exists("histograms.index"):
            os.remove("histograms.index")
        
        prop = rtree.index.Property()
        prop.dimension = len(next(iter(histograms.values()))[0])  # Dimensión del histograma
        prop.buffering_capacity = 3
        prop.dat_extension = "data"
        prop.idx_extension = "index"
        
        rindex = rtree.index.Index('histograms', properties=prop)
        idx = 0
        for label, hist_list in histograms.items():
            for hist in hist_list:
                rindex.insert(idx, hist)
                idx += 1
    
    def loadRIndex(self, file):
        prop = rtree.index.Property()
        prop.dimension = 128  # Ajusta según el tamaño de los histogramas
        prop.buffering_capacity = 3
        prop.dat_extension = "data"
        prop.idx_extension = "index"
        self.ind = rtree.index.Index(file, properties=prop)
    
    def searchknn(self, query_hist, k):
        self.searchResults = self.ind.nearest(query_hist, num_results=k)

class Kdtree:
    def __init__(self):
        self.filename = 'kdtree_histograms.pickle'
        self.ind = []
    
    def GoSecondMemory(self, histograms):
        hist_list = [hist for hists in histograms.values() for hist in hists]
        tree = KDTree(hist_list)
        with open(self.filename, 'wb') as file:
            pickle.dump(tree, file)
    
    def recoveryVector(self):
        with open(self.filename, 'rb') as file:
            return pickle.load(file)
    
    def searchknn(self, query_hist, k):
        tree = self.recoveryVector()
        dist, self.ind = tree.query(query_hist, k=k)
    
    def recoverImgs(self, files):
        images = [files[str(i)] for i in self.ind]
        return images

