from deepforest import main
import matplotlib.pyplot as plt

def predict(image_path, plot=False):
    model = main.deepforest()
    model.use_release()
    return model.predict_image(path=image_path, return_plot=plot)

def show(data):
    plt.imshow(data[:,:,::-1])
    plt.show() 