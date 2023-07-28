from deepforest import main
import os
import matplotlib.pyplot as plt
model = main.deepforest()
model.use_release()

img = model.predict_image(path="./img1.png",return_plot=True)

#predict_image returns plot in BlueGreenRed (opencv style), but matplotlib likes RedGreenBlue, switch the channel order.
plt.imshow(img[:,:,::-1])