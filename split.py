import os
import shutil

def split_data(source_dir, target_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    # lấy folder địa danh trong source 
    places = os.listdir(source_dir)
    
    # lấy path từng cái place
    for place in places:
        place_path = os.path.join(source_dir, place) # path của địa danh
        place_paths = os.listdir(place_path) # path của mấy cái ảnh trong folder 1 địa danh
        
        # tính số ảnh tương ứng với ratio
        n_train = int(len(place_paths) * train_ratio)
        n_val = int(len(place_paths) * val_ratio)

        # tạo dict lưu các key là train,val,test với value là các path đến ảnh
        splits = {
            "train": place_paths[:n_train],
            "val": place_paths[n_train: n_train + n_val],
            "test": place_paths[n_train + n_val:]
        }
        
        # xét qua dict, để chia thành các folder train test val
        for split, imgs in splits.items():
            path = os.path.join(target_dir, split, place)
            os.makedirs(path, exist_ok=True) # tao path cac folder train test val trong target dir
            
            # copy img tu source dir sang target dir
            for img in imgs:
                source_img = os.path.join(source_dir, place, img)
                target_img = os.path.join(path, img)
                shutil.copy2(source_img, target_img)
            
# Call
split_data("D:/REAL PROJECT/landmark_images", "D:/REAL PROJECT/dataset")