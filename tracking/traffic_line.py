
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import numpy as np

class TrafficLine():
    def __init__(self, img_size, max_depth=30):
        self.img_size = img_size
        self.max_depth = max_depth
        self.model = MultiOutputRegressor(RandomForestRegressor(max_depth=self.max_depth,random_state=0))

    def train(self, t, bbox):
        X = np.array([t]).reshape(1,-1)
        threshold = 0.8
    
        for dx in range(-1,2):
            for dy in range(-1, 2):
                for dw in range(-1, 2):
                    for dh in range(-1, 2):
                        Y = np.array([bbox[0]+dx, bbox[1]+dy, bbox[2]+dw, bbox[3]+dh]).reshape(1,-1)
                        self.model.fit(X, Y)

    def predict(self, t):
        X = np.array([t]).reshape(1,-1)
        Y = self.model.predict(X)
        bbox = [Y[0][0], Y[0][1], Y[0][2], Y[0][3]]
        return bbox