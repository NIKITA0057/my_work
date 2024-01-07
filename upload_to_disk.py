import os
import time

import yadisk
import password
from loguru import logger


def get_file_local():
    file_list = os.listdir(password.PATH)
    return file_list


def get_file_yadisk():
    files_of_yandex = []
    client = yadisk.Client(token=password.TOKEN)
    disk_list = client.listdir('/main')
    for ya_file in disk_list:
        files_of_yandex.append(ya_file.name)
    return files_of_yandex


def remove_file(files_list_yandex, file_list_local):
    client = yadisk.Client(token=password.TOKEN)
    for file1 in files_list_yandex:
        if file1 not in set(file_list_local):
            try:
                client.remove(f'/main/{file1}')
                logger.info(f'file {file1} delited')
            except Exception as e:
                logger.error(f'file breake {file1}')


def upload_to_yadisk(files_list_yandex, file_list_local):
    social = yadisk.Client(token=password.TOKEN)
    for file in file_list_local:
        if os.path.basename(file) not in set(files_list_yandex):
            try:
                social.upload(password.PATH + f'/{file}', f'/main/{file}')
                logger.info(f'file upload {file}')
            except Exception as e:
                logger.error(f'file don"t upload {file}')


def update(file_list_local):
    social = yadisk.Client(token=password.TOKEN)
    for update_file in file_list_local:
        social.upload(password.PATH + f'/{update_file}', f'/main/{update_file}', overwrite=True)
    logger.info(f'update file')


# l1 - yadisk
# l2 = localdisk
def main():
    files_list_yandex = get_file_yadisk()
    file_list_local = sorted(get_file_local())
    if len(files_list_yandex) > len(file_list_local):
        remove_file(files_list_yandex, file_list_local)
    elif len(file_list_local) > len(files_list_yandex):
        upload_to_yadisk(files_list_yandex, file_list_local)
    else:
        update(file_list_local)


if __name__ == '__main__':
    while True:
        time.sleep(10)
        main()
