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
    print('rem')
    for i in l1:
        print(i)
        for file in l2:
            if i == file:
                continue
            else:
                logger.info(f'deleated file {i}')
                client.remove(f'/main/{i}')


def upload_to_yadisk(l1, l2):
    social = yadisk.Client(token=password.TOKEN)
    print('up')
    for i in l2:
        for a in l1:
            if i == a:
                continue
            else:
                social.upload(password.PATH + f'/{i}', f'/main/{i}')
                logger.info(f'upload file {i}')


def update(l2):
    social = yadisk.Client(token=password.TOKEN)
    for i in l2:
        social.upload(password.PATH + f'/{i}', f'/main/{i}',overwrite=True)
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