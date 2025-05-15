import cv2
import os
import random
import numpy as np

random.seed(42)

folder_path = r"c:\Users\saher\Desktop\github\cv_projects\Identifying and locating flags from aerial photography\src\data\downloaded_flags"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

flags = [
    os.path.join(folder_path, f)
    for f in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, f))
]
Num_flags = len(flags)

hieght_scaling_values = [5, 10, 15, 20]
brightness_factors = [0.8, 0.6, 0.5, 0.4, 0.3]
final_shape = [24, 27, 30, 32, 35]
back_grounds_path = [
    r"C:\Users\saher\Desktop\github\cv_projects\Identifying and locating flags from aerial photography\src\data\back_grounds\p1.jpg",
    r"C:\Users\saher\Desktop\github\cv_projects\Identifying and locating flags from aerial photography\src\data\back_grounds\p2.jpg",
    r"C:\Users\saher\Desktop\github\cv_projects\Identifying and locating flags from aerial photography\src\data\back_grounds\p6.jpg",
]

edited_flags = r"c:\Users\saher\Desktop\github\cv_projects\Identifying and locating flags from aerial photography\src\data\inserted_flags_in_backgrounds"
if not os.path.exists(edited_flags):
    os.makedirs(edited_flags)

# تحميل الخلفيات مسبقاً
backgrounds = [cv2.imread(path) for path in back_grounds_path]

# التحقق من الخلفيات المحملة
backgrounds = [bg for bg in backgrounds if bg is not None]
if not backgrounds:
    raise ValueError(
        "No valid backgrounds were loaded. Please check the paths in 'back_grounds_path'."
    )

# معرفة حجم الخلفية
back_ground = backgrounds[0]  # Use the first valid background
height, width = back_ground.shape[:2]


def load_image_with_retry(image_path, retries=3):
    """Try to load an image with multiple retries."""
    for attempt in range(retries):
        image = cv2.imread(image_path)
        if image is not None:
            return image
        print(f"Retrying to load image: {image_path} (Attempt {attempt + 1}/{retries})")
    return None


num_of_images_edited = 0
list_image_num_that_edited = []
null_files = []
invalid_files = []


for i in range(0, height - 40, 200):
    for j in range(0, width - 40, 300):
        list_image_num_that_edited.append(num_of_images_edited)
        num_of_images_edited = 0
        for file in range(Num_flags):

            num_of_images_edited += 1
            image = load_image_with_retry(flags[file])

            if image is None and flags[file] not in null_files:
                null_files.append(flags[file])
                invalid_files.append(flags[file])
                print(f"Invalid file detected: {flags[file]}")
                continue

            flage_h, flage_w = image.shape[:2]
            scale = random.choice(hieght_scaling_values)
            small_image = cv2.resize(
                image,
                (flage_w // scale, flage_h // scale),
                interpolation=cv2.INTER_LINEAR,
            )
            pixelated_image = cv2.resize(
                small_image, (flage_w, flage_h), interpolation=cv2.INTER_NEAREST
            )
            final_w = random.choice(final_shape)
            final_h = random.choice(final_shape)
            final_image = cv2.resize(
                pixelated_image, (final_w, final_h), interpolation=cv2.INTER_LINEAR
            )

            brightness_factor = random.choice(brightness_factors)
            darker_image = np.clip(final_image * brightness_factor, 0, 255).astype(
                np.uint8
            )

            back_ground = backgrounds[file % len(backgrounds)].copy()

            # التحقق إن الحجم لا يخرج خارج الخلفية
            if i + 10 + final_h <= height and j + 10 + final_w <= width:
                roi = back_ground[i + 10 : i + 10 + final_h, j + 10 : j + 10 + final_w]
                if roi.shape[:2] == darker_image.shape[:2]:
                    alpha = 0.7
                    blended = cv2.addWeighted(darker_image, alpha, roi, 1 - alpha, 0)
                    back_ground[
                        i + 10 : i + 10 + final_h, j + 10 : j + 10 + final_w
                    ] = blended

                    filename = flags[file].split("\\")[-1].split(".")[0]
                    output_path = os.path.join(
                        edited_flags, f"{filename}_{i}_{j}_{file}.jpg"
                    )
                    cv2.imwrite(output_path, back_ground)
                    print(f"Saved: [{i * j * file}] {output_path}")

print(f"Number of null files: {len(null_files)}")
print(f"Number of null files: {len(null_files)}")
print(f"Number of null files: {len(null_files)}")
if invalid_files:
    print("Invalid files:")
    print("Invalid files:")
    print("Invalid files:")
    for invalid_file in invalid_files:
        print(invalid_file)
print("-" * 50)
print(
    f"the number of images for that you edit in each loop : {np.unique(np.array(list_image_num_that_edited))}"
)
