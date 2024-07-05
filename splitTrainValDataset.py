import math
import os

def split_train_and_validate(train, val, data_index_path, image_txt_path):
    mod = math.floor((train + val) / val)
    dir_name = 'split_' + str(train) + '_' + str(val)
    data_index_path = data_index_path + '/' + dir_name
    new_folder = os.path.exists(data_index_path)
    if not new_folder:
        os.makedirs(data_index_path)

    train_data_index_path = data_index_path + '/train.txt'
    val_data_index_path = data_index_path + '/val.txt'

    count = 0
    train_data_count = 1
    val_data_count = 1
    for root, dirs, files in os.walk(image_txt_path, topdown=True):
        for file_name in files:
            file_name_elements = file_name.split('.')
            if file_name_elements[1] == 'jpg':
                new_file_name = root + '/' + file_name
                print(new_file_name)
                if (count + 1) % mod != 0:
                    # train
                    train_data_count += 1
                    with open(train_data_index_path, 'a+') as train_f:
                        train_f.write(new_file_name + '\n')
                    train_f.close()
                else:
                    # val
                    val_data_count += 1
                    with open(val_data_index_path, 'a+') as val_f:
                        val_f.write(new_file_name + '\n')
                    val_f.close()
                count += 1
    print('the number of train data is : {0}'.format(train_data_count))
    print('the number of val data is : {0}'.format(val_data_count))

if __name__ == "__main__":
    split_train_and_validate(9,1,'/home/wangyu/tmp_data/视觉算法测试题/', '/home/wangyu/tmp_data/视觉算法测试题/elevator_data/data_for_yolo')