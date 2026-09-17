# Traffic

A convolutional neural network (CNN), built with TensorFlow/Keras, that classifies images of German traffic signs into 43 categories.

## Dataset

This project requires the [GTSRB (German Traffic Sign Recognition Benchmark)](https://benchmark.ini.rub.de/) dataset, which is **not included in this repository** (it is roughly 238MB / 26,640 images). Download it separately, e.g. from the CS50AI course site (`https://cdn.cs50.net/ai/2023/x/projects/5/traffic.zip` contains a `gtsrb` folder), and place it alongside `traffic.py` as a `gtsrb/` directory containing one numbered subfolder per category (`gtsrb/0/`, `gtsrb/1/`, ... `gtsrb/42/`), each holding that category's training images. Then run:

```
python traffic.py gtsrb [model.h5]
```

## Model analysis / notes

Through experimenting, I found that more convolutional and pooling layers were beneficial given the limited number of epochs available; the small epoch budget made a stronger architecture necessary rather than optional. Adding more hidden layers helped too, but only once dropout layers were added underneath them, which turned out to be essential rather than optional.

Increasing the number of filters in each successive conv layer also helped. Further reading suggested this is because earlier layers tend to pick up more global features while later layers with more filters pick up finer, more local ones. Conversely, I used a decreasing number of neurons per hidden layer (starting at 64, tapering toward the output size of 10), on the assumption that narrowing the network toward the output size made more sense than keeping it wide throughout, though I'm still not fully certain this was the right call.

Activation functions had the biggest effect of anything I tried. My prior experience suggested ReLU for hidden layers and softmax for the output layer as a safe default, but replacing ReLU with sigmoid in the first conv layer produced a large improvement. From some brief research, this seems to be because ReLU can cause dying neurons: any negative input maps to zero, so a neuron can get stuck outputting zero, whereas sigmoid still produces a non-zero output for negative inputs. At the same time, ReLU worked better in the third layer, where its sharper, more decisive outputs were useful. For the middle conv/pooling layer I used leaky ReLU, which sits between ReLU and sigmoid: sigmoid can cause vanishing gradients and leaky ReLU avoids that while still handling negative inputs better than plain ReLU. Changing the second layer from ReLU to leaky ReLU also produced a small improvement.

This left me thinking about how much the choice of activation function matters per layer, and how the conv/pooling backbone in particular seems to be the most sensitive part of the architecture for a given dataset, though I don't yet have a reliable way to tune this beyond trial and error.

Using sigmoid across multiple conv layers made the model worse, but mixing activation function types across layers kept helping: using tanh in the middle layer gave results close to the leaky ReLU version (49% accuracy versus 50-53% for leaky ReLU). My main takeaway for future computer vision work is that using different activation functions across conv layers, rather than one function throughout, has a measurable effect on accuracy.
