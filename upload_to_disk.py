import os
import time

import yadisk
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


def get_file_local():
    """Получает список файлов в локальной папке."""
    file_list = os.listdir(os.getenv("LOCAL_PATH"))
    return file_list


def get_file_yadisk(client):
    """Получает список файлов на Яндекс.Диске."""
    files_of_yandex = []
    disk_list = client.listdir("/main")
    for ya_file in disk_list:
        files_of_yandex.append(ya_file.name)
    return files_of_yandex


def remove_file(files_list_yandex, file_list_local, client):
    """Удаляет файлы на Яндекс.Диске, которых нет в локальной папке."""
    for file1 in files_list_yandex:
        if file1 not in set(file_list_local):
            try:
                client.remove(f"/main/{file1}")
                logger.info(f"file {file1} delited")
            except Exception as e:
                logger.error(f"file breake {file1}")


def upload_to_yadisk(files_list_yandex, file_list_local, social):
    """Загружает файлы из локальной папки на Яндекс.Диск."""
    for file in file_list_local:
        if os.path.basename(file) not in set(files_list_yandex):
            try:
                social.upload(os.getenv("LOCAL_PATH") + f"/{file}", f"/main/{file}")
                logger.info(f"file upload {file}")
            except Exception as e:
                logger.error(f'file don"t upload {file}')


def update_files(file_list_local, social):
    """Обновляет файлы на Яндекс.Диске из локальной папки."""
    for update_file in file_list_local:
        social.upload(
            os.getenv("LOCAL_PATH") + f"/{update_file}",
            f"/main/{update_file}",
            overwrite=True,
        )
    logger.info(f"update file")


def main():
    """Основная функция, выполняющая сравнение и синхронизацию файлов."""
    client = yadisk.Client(token=os.getenv("TOKEN"))
    files_list_yandex = get_file_yadisk(client)
    file_list_local = sorted(get_file_local())
    if len(files_list_yandex) > len(file_list_local):
        remove_file(files_list_yandex, file_list_local, client)
    elif len(file_list_local) > len(files_list_yandex):
        upload_to_yadisk(files_list_yandex, file_list_local, client)
    else:
        update_files(file_list_local, client)


if __name__ == "__main__":
    while True:
        time.sleep(10)
        main()
