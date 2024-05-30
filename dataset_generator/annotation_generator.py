import json
import glob
import os
from tqdm import tqdm

def generate_annotation():
    original_width = 3840
    original_height = 2160
    new_width = 640
    new_height = 640

    files = glob.glob('/Users/jaeh/Documents/NVIDIA_AI_Academy/CV_Project/test_data/2120699/*')
    image_frames = [int(os.path.splitext(os.path.basename(file))[0].split('_')[1]) for file in files if os.path.isfile(file)]
    image_frames.sort()

    with open('/Users/jaeh/Documents/NVIDIA_AI_Academy/CV_Project/test_data/annotation_2120699.json') as f:
        data = json.load(f)

        for frame in data['frames']:
            if frame['number'] in image_frames:
                print(frame['number'])
                annot = []
                for annotation in frame['annotations']:
                    label = annotation['label']
                    x_min = label['x']
                    y_min = label['y']
                    width = label['width']
                    height = label['height']
                    
                    ## convert to center coordinates
                    x_center = x_min + width / 2
                    y_center = y_min + height / 2
                    
                    ## scale the center coordinates and dimensions
                    x_center_new = x_center * new_width / original_width
                    y_center_new = y_center * new_height / original_height
                    width_new = width * new_width / original_width
                    height_new = height * new_height / original_height

                    x_center_norm = x_center_new / new_width
                    y_center_norm = y_center_new / new_height
                    width_norm = width_new / new_width
                    height_norm = height_new / new_width

                    annot.append(f"0 {x_center_norm} {y_center_norm} {width_norm} {height_norm}")
                    

                with open(f"/Users/jaeh/Documents/NVIDIA_AI_Academy/CV_Project/test_data/generated_annotations/frame_{frame['number']}.txt", "w") as txt:
                    for i in range(len(annot)):
                        if i == (len(annot) - 1):
                            txt.write(f"{annot[i]}")
                        else:
                            txt.write(f"{annot[i]}\n")


def remove_file_annot(image_folder, annot_folder):
    image_files = sorted(glob.glob(image_folder))
    annot_files = sorted(glob.glob(annot_folder))

    for image_file, annot_file in tqdm(zip(image_files, annot_files), total = len(image_files)):
        with open(annot_file) as f2:
            # label_list = [[[int(value)] for value in item.split()] for item in f2.readlines()]
            labels = [int(item.split()[0]) for item in f2.readlines()]
            # print(labels)
            if 5 not in labels:
                # print(image_file, annot_file)
                os.remove(image_file)
                os.remove(annot_file)

            



if __name__ == "__main__":
    # generate_annotation()
    remove_file_annot('/Users/jaeh/Downloads/train_img/train_img/*', '/Users/jaeh/Downloads/train_label/train_label/*')