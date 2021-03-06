import numpy as np
from skimage.transform import resize
from skimage.util import pad
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import keras
import sys


def create_classifier():
    # use old classifier
    model = keras.models.load_model("mnist_model.keras")
    return model, 28, 28


def parse(d, clf, nrows, ncols):
    # width and height of canvas
    width, height = d["width"], d["height"]
    # canvas as matrix
    M = np.zeros((height, width))
    for line in d["lines"]:
        # must be an even number. also, brushsize is too small
        brushsize = line["brushRadius"] * 2

        kernel = np.ones((brushsize, brushsize))
        for point in line["points"]:
            x, y = int(point["x"]), int(point["y"])
            # clamp x and y inside canvas
            x = max(min(x, width), 0)
            y = max(min(y, height), 0)

            # clamp x and y inside canvas
            x = max(min(x, width), 0)
            y = max(min(y, height), 0)
            
            # how much the kernel goes outside the canvas on each side
            topout = max(brushsize // 2 - y, 0)
            bottonout = max(brushsize // 2 + y - height, 0)
            leftout = max(brushsize // 2 - x, 0)
            rightout = max(brushsize // 2 + x - width, 0)

            # corners of the window
            t = y - brushsize // 2 + topout
            b = y + brushsize // 2 - bottonout
            l = x - brushsize // 2 + leftout
            r = x + brushsize // 2 - rightout

            # cropped to not extend outside canvas
            cropped_kernel = kernel[
                topout : brushsize - bottonout, leftout : brushsize - rightout
            ]
            M[t:b, l:r] = cropped_kernel

    # same size as training images 28x28
    smaller = resize(M, (nrows, ncols))
    # same dimentions and intensity scale as training image
    scaled = smaller.reshape((1, nrows, ncols, 1)) * 255

    if __name__ == "__main__":
        from matplotlib import pyplot as plt
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow((scaled.reshape((nrows, ncols))))
        ax2.imshow(M)
        plt.show()

    # predict digit. returns onehot signal
    onehot, *_ = clf.predict(scaled)
    # find index of onehot signal. this is the actual number
    prediction = np.argmax(onehot, axis=0)

    return prediction


if __name__ == "__main__":
    ex = {
        "lines": [
            {
                "points": [
                    {"x": 225.90390270001288, "y": 109.72082940320792},
                    {"x": 225.90390270001288, "y": 109.72082940320792},
                    {"x": 225.90390270001288, "y": 109.72082940320792},
                    {"x": 225.90390270001288, "y": 109.72082940320792},
                    {"x": 225.4382073819436, "y": 109.36466343640411},
                    {"x": 208.39592591869416, "y": 108.95918431172036},
                    {"x": 194.12243343109742, "y": 111.80297469076098},
                    {"x": 185.76202966276418, "y": 114.37797319887416},
                    {"x": 167.29163657627495, "y": 122.076596759019},
                    {"x": 146.41889660108805, "y": 134.32756675295607},
                    {"x": 139.08011060089467, "y": 140.41932402610715},
                    {"x": 134.4845879170673, "y": 144.74583204923167},
                    {"x": 129.3720575983839, "y": 151.90049818477266},
                    {"x": 126.62825973544517, "y": 158.36213391679084},
                    {"x": 125.04017202694669, "y": 163.7950548304013},
                    {"x": 126.14168311003851, "y": 182.24227159672236},
                    {"x": 132.54484196269385, "y": 201.92318240795106},
                    {"x": 138.91117278981977, "y": 215.56729388072287},
                    {"x": 156.49044469180305, "y": 244.32982292720976},
                    {"x": 169.66200520620288, "y": 262.8762324733901},
                    {"x": 182.22037243919056, "y": 279.2027237261216},
                    {"x": 197.9043739573412, "y": 298.45290648173585},
                    {"x": 209.43579133984372, "y": 314.0402128521089},
                    {"x": 221.77955862575388, "y": 331.7936257928262},
                    {"x": 231.01068577568023, "y": 345.6362322222667},
                    {"x": 238.8037802366376, "y": 359.14372112983204},
                    {"x": 243.8005508500321, "y": 369.6194832275025},
                    {"x": 250.24278956315294, "y": 388.025165882883},
                    {"x": 253.68799607625851, "y": 402.60272457365653},
                    {"x": 254.34950003095173, "y": 417.2313689201361},
                    {"x": 254.24684753177402, "y": 423.2187846102349},
                    {"x": 251.10015251620962, "y": 433.8127290698992},
                    {"x": 239.43645009626078, "y": 449.9467796797072},
                    {"x": 234.7569882093908, "y": 455.02605110436434},
                    {"x": 224.98570979888075, "y": 463.3067718051383},
                    {"x": 213.13810979957663, "y": 470.86900515056374},
                    {"x": 197.3554074459488, "y": 477.2321453283286},
                    {"x": 191.07713753802548, "y": 478.58447498448527},
                    {"x": 183.34313654195194, "y": 477.89511859808727},
                    {"x": 173.74723852442617, "y": 474.9030929630168},
                    {"x": 169.27027490907972, "y": 472.15326963631554},
                    {"x": 161.94222086499994, "y": 462.9036827439362},
                    {"x": 155.85006099991216, "y": 432.73180781833184},
                    {"x": 154.40290062932573, "y": 417.94816791877776},
                    {"x": 153.55562598760218, "y": 396.0059452556725},
                    {"x": 156.34395522291666, "y": 371.921126597097},
                    {"x": 160.94818353630788, "y": 350.6895652143968},
                    {"x": 167.30869452768331, "y": 332.2310600928357},
                    {"x": 174.6353804992249, "y": 313.9800835945254},
                    {"x": 186.9304787797017, "y": 292.16186179317936},
                    {"x": 200.19218964005648, "y": 275.00887992916756},
                    {"x": 213.03098847711576, "y": 258.8824057965585},
                    {"x": 226.22837316865295, "y": 247.17344929958492},
                    {"x": 233.91260274771741, "y": 240.80522800990337},
                    {"x": 247.34165296573417, "y": 231.06906152383604},
                    {"x": 251.39059720211597, "y": 227.35322724473596},
                    {"x": 252.873271515933, "y": 225.8543134600989},
                    {"x": 255.8602018662684, "y": 221.4953759684674},
                    {"x": 258.7251748111611, "y": 215.57763196975313},
                    {"x": 261.2785355413819, "y": 208.22063038025664},
                    {"x": 264.3436509083574, "y": 196.54473788968627},
                    {"x": 265.82484369004095, "y": 186.85143933603794},
                    {"x": 266.0739001378661, "y": 182.98685794993807},
                    {"x": 262.8675841770756, "y": 171.4875660273449},
                    {"x": 258.40784398304766, "y": 162.5123864202025},
                    {"x": 256.33432151380714, "y": 159.00891337000027},
                    {"x": 251.45230981534783, "y": 152.27507591594076},
                    {"x": 236.96683348204414, "y": 139.94879404201015},
                    {"x": 207.58567208077304, "y": 123.61387230513039},
                    {"x": 195.41248823440768, "y": 118.85738996468852},
                    {"x": 185.75711250788507, "y": 115.87129623426947},
                    {"x": 184.56566911172257, "y": 115.44705393956191},
                    {"x": 184.56566911172257, "y": 115.44705393956191},
                ],
                "brushColor": "#663399",
                "brushRadius": 5,
            }
        ],
        "width": 400,
        "height": 600,
    }

    clf, nrows, ncols = create_classifier()
    p = parse(ex, clf, nrows, ncols)
    print(p)
