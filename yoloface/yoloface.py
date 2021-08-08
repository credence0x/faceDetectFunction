# *******************************************************************

# EDITED BY Lanre Ojetokun to only cater for images and to work 
# specifically with my face detection app

# Original Author : Thanh Nguyen, 2018 
# Email  : sthanhng@gmail.com
# Github : https://github.com/sthanhng
#
# BAP, AI Team
# Face detection using the YOLOv3 algorithm
#
# Description : yoloface.py
# The main code of the Face detection using the YOLOv3 algorithm
#
# *******************************************************************

# Usage example:  python yoloface.py --image samples/outside_000001.jpg \
#                                    --output-dir outputs/
#                 python yoloface.py --video samples/subway.mp4 \
#                                    --output-dir outputs/
#                 python yoloface.py --src 1 --output-dir outputs/


import argparse
import sys
import os

from yoloface.utils import *
def run_yoloface(image_path,model_cfg,model_weights,output_dir):
    image = image_path
    if not model_cfg:
        model_cfg = './cfg/yolov3-face.cfg'
    if not model_weights:
        model_weights = './model-weights/yolov3-wider_16000.weights'
    if not output_dir:
        output_dir = 'outputs/'



    #####################################################################
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--model-cfg', type=str, default='./cfg/yolov3-face.cfg',
    #                     help='path to config file')
    # parser.add_argument('--model-weights', type=str,
    #                     default='./model-weights/yolov3-wider_16000.weights',
    #                     help='path to weights of model')
    # parser.add_argument('--image', type=str, default='',
    #                     help='path to image file')


    # parser.add_argument('--output-dir', type=str, default='outputs/',
    #                     help='path to the output directory')
    # args = parser.parse_args()

    #####################################################################
    # print the arguments
    # print('----- info -----')
    # print('[i] The config file: ', args.model_cfg)
    # print('[i] The weights of model file: ', args.model_weights)
    # print('[i] Path to image file: ', args.image)
    # print('[i] Path to video file: ', args.video)
    # print('###########################################################\n')

    # check outputs directory
    if not os.path.exists(output_dir):
        print('==> Creating the {} directory...'.format(output_dir))
        os.makedirs(output_dir)
    else:
        print('==> Skipping create the {} directory...'.format(output_dir))

    # Give the configuration and weight files for the model and load the network
    # using them.
    net = cv2.dnn.readNetFromDarknet(model_cfg, model_weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def _main():
        wind_name = 'face detection using YOLOv3'
        # cv2.namedWindow(wind_name, cv2.WINDOW_NORMAL)

        output_file = ''

        if image:
            if not os.path.isfile(image):
                print("[!] ==> Input image file {} doesn't exist".format(image))
                sys.exit(1)
            cap = cv2.VideoCapture(image)
            output_file = image[:-4].rsplit('/')[-1] + '_yoloface.jpg'
        
        while True:

            has_frame, frame = cap.read()
            # Stop the program if reached end of video
            if not has_frame:
                print('[i] ==> Done processing!!!')
                print('[i] ==> Output file is stored at', os.path.join(output_dir, output_file))
                cv2.waitKey(1000)
                break
            # print(frame.shape) #(x,x,3)

            # Create a 4D blob from a frame.
            blob = cv2.dnn.blobFromImage(frame, 1 / 255, (IMG_WIDTH, IMG_HEIGHT),
                                         [0, 0, 0], 1, crop=False)

            # Sets the input to the network
            net.setInput(blob)

            # Runs the forward pass to get output of the output layers
            outs = net.forward(get_outputs_names(net))

            # Remove the bounding boxes with low confidence
            faces = post_process(frame, outs, CONF_THRESHOLD, NMS_THRESHOLD)
            print('[i] ==> # detected faces: {}'.format(len(faces)))

            # initialize the set of information we'll displaying on the frame
            info = [
                #LANRE
                # ('number of faces detected', '{}'.format(len(faces)))
            ]

            # for (i, (txt, val)) in enumerate(info):
            #     text = '{}: {}'.format(txt, val)
            #     cv2.putText(frame, text, (10, (i * 20) + 20),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_RED, 2)

            
            cv2.imwrite(os.path.join(output_dir, output_file), frame.astype(np.uint8))



        print('DONE!')

        print('***********************************************************')
        file_path = os.path.join(output_dir, output_file)
        return file_path,len(faces)


    #call the main function
    file_path,number_of_faces = _main()
    return file_path,number_of_faces


# if __name__ == '__main__':
#     _main()
