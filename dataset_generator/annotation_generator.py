import json
import glob
import os
from tqdm import tqdm
from pathlib import Path


"""
Label information

0: 폭행
1: 실신
2: 기물파손
3: 절도
4: 이동상인
5: 몰카
6: 자전거 승차

"""

annotation_labels = {
    "폭행" : 0,
    "실신" : 1,
    "기물파손" : 2,
    "절도" : 3,
    "이동상인" : 4,
    "몰카" : 5,
    "자전거 승차" : 6,
}

json_labels = {
    "assault" : 0,
    "fainting" : 1,
    "property_damage" : 2,
    "theft" : 3,
    "spy_camera" : 5
}

def generate_annotation(image_parent, annot_parent):
    original_width = 3840
    original_height = 2160
    new_width = 640
    new_height = 640

    # Get ids of video file from annotation files
    annot_file_ids = sorted([Path(file).stem.split('_')[1] for file in glob.glob(annot_parent + '/*')])

    # Iterate over all video files
    for id in tqdm(annot_file_ids):

        # Load json annotation file
        with open(annot_parent + f'/annotation_{id}.json', encoding = 'utf-8') as f:
            data = json.load(f)
            # Get frame numbers
            annot_frame_numbers = [str(value) for i in range(len(data['frames'])) for key, value in data['frames'][i].items() if key == "number"]

        # Get image files
        image_files = sorted(glob.glob(image_parent + f'/{id}/*'))
        image_frames = [Path(file).stem.split('_')[1] for file in image_files]
        
        # Delete image file if frame is not annotated
        for frame in image_frames:
            if frame not in annot_frame_numbers:
                os.remove(image_parent + f'/{id}/frame_{frame}.jpg')
        
        # Create annotation text file
        for frame in data['frames']:
            if str(frame['number']) in image_frames:
                annot = []

                for annotation in frame['annotations']:
                    label = annotation['label']
                    category = json_labels[annotation['category']['code']]

                    # Get original coordination
                    x_min = label['x']
                    y_min = label['y']
                    width = label['width']
                    height = label['height']
                    
                    # Convert to center coordinates
                    x_center = x_min + width / 2
                    y_center = y_min + height / 2
                    
                    # Scale the center coordinates and dimensions
                    x_center_new = x_center * new_width / original_width
                    y_center_new = y_center * new_height / original_height
                    width_new = width * new_width / original_width
                    height_new = height * new_height / original_height

                    x_center_norm = x_center_new / new_width
                    y_center_norm = y_center_new / new_height
                    width_norm = width_new / new_width
                    height_norm = height_new / new_width

                    annot.append(f"{category} {x_center_norm} {y_center_norm} {width_norm} {height_norm}")
                    
                if not os.path.exists(image_parent + f'/{id}_annotation'):
                    os.makedirs(image_parent + f'/{id}_annotation')
                    with open(image_parent + f"/{id}_annotation/frame_{frame['number']}.txt", "w") as txt:
                        for i in range(len(annot)):
                            txt.write(f"{annot[i]}\n")
                else:
                    with open(image_parent + f"/{id}_annotation/frame_{frame['number']}.txt", "w") as txt:
                            for i in range(len(annot)):
                                txt.write(f"{annot[i]}\n")




    ###############################################################################################
    # image_frames = [int(os.path.splitext(os.path.basename(file))[0].split('_')[1]) for file in files if os.path.isfile(file)]
    # image_frames.sort()

    # with open('/Users/jaeh/Documents/NVIDIA_AI_Academy/CV_Project/test_data/annotation_2120699.json') as f:
    #     data = json.load(f)

    #     for frame in data['frames']:
    #         if frame['number'] in image_frames:
    #             print(frame['number'])
    #             annot = []
    #             for annotation in frame['annotations']:
    #                 label = annotation['label']
    #                 x_min = label['x']
    #                 y_min = label['y']
    #                 width = label['width']
    #                 height = label['height']
                    
    #                 # convert to center coordinates
    #                 x_center = x_min + width / 2
    #                 y_center = y_min + height / 2
                    
    #                 # scale the center coordinates and dimensions
    #                 x_center_new = x_center * new_width / original_width
    #                 y_center_new = y_center * new_height / original_height
    #                 width_new = width * new_width / original_width
    #                 height_new = height * new_height / original_height

    #                 x_center_norm = x_center_new / new_width
    #                 y_center_norm = y_center_new / new_height
    #                 width_norm = width_new / new_width
    #                 height_norm = height_new / new_width

    #                 annot.append(f"0 {x_center_norm} {y_center_norm} {width_norm} {height_norm}")
                    

    #             with open(f"/Users/jaeh/Documents/NVIDIA_AI_Academy/CV_Project/test_data/generated_annotations/frame_{frame['number']}.txt", "w") as txt:
    #                 for i in range(len(annot)):
    #                     if i == (len(annot) - 1):
    #                         txt.write(f"{annot[i]}")
    #                     else:
    #                         txt.write(f"{annot[i]}\n")


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


def match_files(image_folder, annot_folder):
    image_files = sorted(glob.glob(image_folder))
    annot_files = sorted(glob.glob(annot_folder))

    image_file_names = [Path(file).stem for file in sorted(glob.glob(image_folder))]
    annot_files_names = [Path(file).stem for file in sorted(glob.glob(annot_folder))]

    # Delete image file without annotation
    for file in image_files:
        if Path(file).stem not in annot_files_names:
            image_file_names.remove(Path(file).stem)
            os.remove(file)

    # Delete annotation file without image
    for file in annot_files:
        if Path(file).stem not in image_file_names:
            annot_files_names.remove(Path(file).stem)
            os.remove(file)

    print("Image and annotation match" if image_file_names == annot_files_names else "Image and annotation does not match")

            
def add_annot_info_file(image_folder, annot_folder, original_label, new_label):
    # Delete image/annotation file if not match
    match_files(image_folder, annot_folder)

    image_files = sorted(glob.glob(image_folder))
    annot_files = sorted(glob.glob(annot_folder))

    # Relabel annotation file
    for (image_file, annot_file) in zip(image_files, annot_files):
        annotation = []
        with open(annot_file, "r") as f:
            labels = [item.strip() for item in f.readlines()]
            for label in labels:
                if label.split(' ')[0] == f'{original_label}':
                    annotation.append(label.replace(f'{original_label}', f'{new_label}', 1))

        if len(annotation) == 0:
            os.remove(annot_file)
            os.remove(image_file)
        else:
            with open(annot_file, "w") as f:
                for line in annotation:
                    f.write(line + "\n")



if __name__ == "__main__":
    generate_annotation('C:/Users/hancom09/Downloads/CV_CCTV/CV_Project/test_data', 'C:/Users/hancom09/Downloads/CV_CCTV/CV_Project/test_data/annotation')

    # remove_file_annot('/Users/jaeh/Downloads/train_img/train_img/*', '/Users/jaeh/Downloads/train_label/train_label/*')

    # add_annot_info_file('/Users/jaeh/Downloads/bicycle/*', '/Users/jaeh/Downloads/bicycle_annotated/*', 1, 7)