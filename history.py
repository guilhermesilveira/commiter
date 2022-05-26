import logging
import os
from pathlib import Path

import pygit2
from PIL import Image

SSH_KEY_PRIVATE = 'keys/id_ed25519'
SSH_KEY_PUBLIC = 'keys/id_ed25519.pub'


class History:
    user_name = "Guilherme Silveira"
    user_mail = "guilherme.silveira@gmail.com"

    def __init__(self, folder: Path):
        self.__repo = pygit2.Repository(folder / ".git")
        self.__base_folder = folder

    def commit_and_push(self, camera_id: int, frame_number: int, path: Path):
        path = path.relative_to(self.__base_folder)
        logging.info(f"Commiting {path}")
        # index
        index = self.__repo.index
        index.add(str(path))
        index.write()

        # commit
        # reference = 'refs/HEAD'
        message = f'camera #{camera_id} frame #{frame_number}'
        tree = index.write_tree()

        author = pygit2.Signature(self.user_name, self.user_mail)

        ref = self.__repo.head.name
        parents = [self.__repo.head.target]
        # ref = "HEAD"
        # parents = []
        oid = self.__repo.create_commit(ref, author, author, message, tree, parents)

        tag_name = f"{frame_number}_{camera_id}"
        oid_tag = self.__repo.create_tag(tag_name, oid, pygit2.GIT_OBJ_COMMIT, author, message)

        logging.info(f"Commited {oid} and {oid_tag}")
        ssh_credentials = pygit2.credentials.Keypair('git', SSH_KEY_PUBLIC, SSH_KEY_PRIVATE, '')
        remote = self.__repo.remotes['origin']
        remote.credentials = ssh_credentials
        callbacks = pygit2.RemoteCallbacks(credentials=ssh_credentials)

        remote.push([ref, f'refs/tags/{tag_name}'], callbacks=callbacks)
        print(f"Pushed")


class Saver:
    def __init__(self, history: History, folder: Path):
        self.__history = history
        self.__current_count = 0
        self.__folder = folder
        os.makedirs(folder, exist_ok=True)
        print(f"Saving to {folder}")

    def trigger(self, camera_id, image, frame_number, delta_info):
        self.__current_count += 1
        # path = self.__folder / f"output_{timestamp}_{self.__current_count}_{frame_number}.jpg"
        path = self.__folder / f"output_{camera_id}.jpg"
        logging.info(f"Triggered {path} {delta_info}")
        pil_image = Image.fromarray(image)
        pil_image.save(str(path), format="jpeg")
        self.__history.commit_and_push(camera_id, frame_number, path)
