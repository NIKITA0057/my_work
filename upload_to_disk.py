import os
import time

import yadisk
import password
from loguru import logger



def get_file_local():
    file_list = os.listdir(password.PATH)
    return file_list


def get_file_yadisk():
    l1 = []
    client = yadisk.Client(token=password.TOKEN)
    disk_list = client.listdir('/main')
    for i in disk_list:
        l1.append(i.name)
    return l1





def remove_file(l1, l2):
    client = yadisk.Client(token=password.TOKEN)

    for file1 in l1:

        for file2 in l2:
            if file1 == file2:
                continue
            else:
                logger.info(f'deleated file {file1}')
                client.remove(f'/main/{file1}')


def upload_to_yadisk(l1, l2):
    social = yadisk.Client(token=password.TOKEN)

    for file2 in l2:
        if len(l1) != 0:
            for file1 in l1:
                if file2 == file1:
                    continue
                else:
                    social.upload(password.PATH + f'/{file2}', f'/main/{file2}')
                    logger.info(f'upload file {file2}')
        else:
            social.upload(password.PATH + f'/{file2}', f'/main/{file2}')
            logger.info(f'upload file {file2}')

def update(l2):
    social = yadisk.Client(token=password.TOKEN)
    for update_file in l2:
        social.upload(password.PATH + f'/{update_file}', f'/main/{update_file}',overwrite=True)
    logger.info(f'update file')



# l1 - yadisk
# l2 = localdisk
def main():
    l1 = get_file_yadisk()
    l2 = sorted(get_file_local())
    if len(l1) > len(l2):
        remove_file(l1, l2)
    elif len(l2) > len(l1):
        upload_to_yadisk(l1, l2)
    else:
        update(l2)

if __name__ == '__main__':
    while True:
        time.sleep(10)
        main()