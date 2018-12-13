from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

class CentroidTracker():
    def __init__(self, maxDisappeared=50):
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.maxDisappeared = maxDisappeared
        
    def register(self, centroid):
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1
        
    def deregister(self, objectID):
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):
        if len(rects) == 0:
            for objectID in self.disappeared.keys():
                self.disappeared[objectID] +=1

                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            
            return self.objects
        
        inputCentroids = np.zeros((len(rects), 2), dtype="int")

        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)
        
        if len(self.objects) == 0:
            for i in range(0, inputCentroids[i]):
                self.register(inputCentroids[i])
        else:
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.value())
            # po porstu min zwraca min wartosc z kazdej koluny [..],[..], arg.sort zwraca indexy do tych wierszy
            # argmin zwraca index do min elementu z kazdego wiersza, kazdy element zwrocony odnosi się do wierszu na ktorym idnex listy wskazuje
            # wystarczy teraz pozortowac, albo raczej poprzestawiac wedlug kolejnosci rows, aby otrzymac odpowiednia kolejnoc 
            # wtdy row i cols, zip stanowią pary punktów
            D = dist.cdist(np.array(objectCentroids), inputCentroids)
            rows = D.min(axis=1).argsort() #min dla wartosci w tabeli dla każdego z wierszu i sortowanie zwróconych indexów

            cols = D.argmin(axis=1)[rows] #zwraca pary pcentroidow dla ktorych wynik jest najniejszy i filtrujemy ten wynik tablica a indexami do najmneijszych warotsci po weirszach by dostac kolumny czyli nowy centroid

            usedRows = set()
            usedCols = set()

            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue
                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0
                
                # indicate that we have examined each of the row and
                # column indexes, respectively
                usedRows.add(row)
                usedCols.add(col)

            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            # in the event that the number of object centroids is
            # equal or greater than the number of input centroids
            # we need to check and see if some of these objects have
            # potentially disappeared
            if D.shape[0] >= D.shape[1]:
                # loop over the unused row indexes
                for row in unusedRows:
                    # grab the object ID for the corresponding row
                    # index and increment the disappeared counter
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1

                    # check to see if the number of consecutive
                    # frames the object has been marked "disappeared"
                    # for warrants deregistering the object
                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)
                    # otherwise, if the number of input centroids is greater
                    # than the number of existing object centroids we need to
                    # register each new input centroid as a trackable object
            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])
        
        # return the set of trackable objects
        return self.objects
