import json
import glob
import os
from tqdm import tqdm
from pathlib import Path
from send2trash import send2trash


"""
Label information

0: 폭행
1: 실신
2: 기물파손
3: 절도
4: 이동상인
5: 몰카

"""

annotation_labels = {
    "assault" : 0,
    "fainting" : 1,
    "property_damage" : 2,
    "theft" : 3,
    "merchant" : 4,
    "spy_camera" : 5,
    "bicycle" : 6
}

def generate_annotation(image_parent, annot_parent):
    original_width = 3840
    original_height = 2160
    new_width = 640
    new_height = 640
    image_num = 0
    label_count = [0, 0, 0, 0, 0, 0, 0]

    # Get ids of video folder from annotation files: ['xxxxxxx']
    annot_file_ids = sorted([Path(file).stem.split('_')[1] for file in glob.glob(annot_parent + '/*')])

    # Iterate over all video files
    for id in tqdm(annot_file_ids):

        # Load json annotation file
        with open(annot_parent + f'/annotation_{id}.json', encoding = 'utf-8') as f:
            data = json.load(f)
            # Get image file names from annotation: ['frame_xxxx.jpg']
            annot_frame_numbers = [value for i in range(len(data['frames'])) for key, value in data['frames'][i].items() if key == "image"]

        # Get image file names: ['frame_xxxx.jpg']
        image_files = [os.path.basename(file) for file in sorted(glob.glob(image_parent + f'/{id}/*'))]
        
        # Delete image file if frame is not annotated
        for filename in image_files:
            if filename not in annot_frame_numbers:
                print(f"Image file {filename} not annotated. Discarding.")
                image_files.remove(filename)
                send2trash(Path(image_parent + f'/{filename}'))
        
        # Create annotation text file
        for frame in data['frames']:
            # If 'frame_xxxx.jpg' in ['frame_xxxx.jpg']
            if frame['image'] in image_files:
                annot = []

                # Get annotation data from data['frames'][i]
                for annotation in frame['annotations']:
                    # Coordinates info
                    label = annotation['label']

                    # Class info
                    try:
                        category = annotation_labels[annotation['category']['code']]
                        label_count[category] += 1
                        image_num += 1
                        current_cat = annotation['category']['code']
                    except:
                        # If class not exists in custom labels, skip recording current coordinates
                        # print(f"No category: {annotation['category']['code']}")
                        continue

                    # Get original coordination
                    x_min = label['x']
                    y_min = label['y']
                    width = label['width']
                    height = label['height']
                    
                    # Convert to center coordinates
                    x_center = x_min + width / 2
                    y_center = y_min + height / 2
                    
                    # Scale, normalize the center coordinates and dimensions
                    x_center_new = x_center * new_width / original_width
                    y_center_new = y_center * new_height / original_height
                    width_new = width * new_width / original_width
                    height_new = height * new_height / original_height

                    x_center_norm = x_center_new / new_width
                    y_center_norm = y_center_new / new_height
                    width_norm = width_new / new_width
                    height_norm = height_new / new_width

                    annot.append(f"{category} {x_center_norm} {y_center_norm} {width_norm} {height_norm}")
                
                # If len(annot) is not 0 -> annotation with custom label exists
                # save image file as '<label><num>.jpg'
                # save annotation txt file as '<label><num>.txt'
                if len(annot) != 0:
                    # Make annotation txt file
                    with open(image_parent + f"/{image_num}_{current_cat}.txt", "w") as txt:
                            for i in range(len(annot)):
                                txt.write(f"{annot[i]}\n")
                    os.rename(image_parent + f"/{id}/{frame['image']}", image_parent + f"/{image_num}_{current_cat}.jpg")
                # If len(annot) is 0 -> annotation with custom label does not exist
                # delete image file
                else:
                    print(f"No usable annotation with frame. Image discarded: {frame['image']}.")
                    send2trash(Path(image_parent + f"/{id}/{frame['image']}"))

    with open('D:/label_counts.txt', "w") as label:
        print("assault: ", label_count[0])
        print("fainting: ", label_count[1])
        print("property_damage: ", label_count[2])
        print("theft: ", label_count[3])
        print("merchant: ", label_count[4])
        print("spy_camera: ", label_count[5])

        label.write("assault: ", label_count[0], '\n')
        label.write("fainting: ", label_count[1], '\n')
        label.write("property_damage: ", label_count[2], '\n')
        label.write("theft: ", label_count[3], '\n')
        label.write("merchant: ", label_count[4], '\n')
        label.write("spy_camera: ", label_count[5], '\n')


def check_missing_folder(image_parent, annot_parent):
    count = 0
    # Get ids of video folder from annotation files: ['xxxxxxx']
    annot_folder_ids = sorted([Path(file).stem.split('_')[1] for file in glob.glob(annot_parent + '/*')])

    # Get ids of video folder from video parent folder: ['xxxxxxx']
    image_folder_ids = sorted(Path(folder).stem for folder in glob.glob(image_parent + '/*'))

    # Check image forlder without annotation
    for img_folder in image_folder_ids:
        if img_folder not in annot_folder_ids:
            count += 1
            print(f'{img_folder} not annotated')
    
    # Check annotation file without image folder
    for annot_folder in annot_folder_ids:
        if annot_folder not in image_folder_ids:
            count += 1
            print(f'{annot_folder} does not have corresponding image folder')
    
    if(count == 0):
        print("Annotation and image folder match")



def relabel():
    annot_files = sorted(glob.glob('D:/Downloads/Downloads/bicycle_annotated/*'))

    # Relabel annotation file
    for annot_file in annot_files:
        annotation = []
        with open(annot_file, "r") as f:
            labels = [item.strip() for item in f.readlines()]
            for label in labels:
                annotation.append(label.replace('7', '6', 1))

        with open(annot_file, "w") as f:
            for line in annotation:
                f.write(line + "\n")



if __name__ == "__main__":
    # generate_annotation('D:/Datasets', 'C:/Users/hancom09/Desktop/annotation')
    # check_missing_folder('D:/Datasets', 'C:/Users/hancom09/Desktop/annotation')
    relabel()


    ## 143401 files, 1312 folders