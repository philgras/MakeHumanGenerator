import os
import numpy as np
import json
from hashlib import sha256

class RandomHuman:
    """
    Generates a random human 3D model by randomly selecting assets and a model from the makehuman user directory
    The random selection in terms of filenames can be accessed through this class.
    """

    def __init__(self, mh_dir):
        """
        Selects human attributes (files) randomly based on the makehuman user directory
        :param mh_dir: MakeHuman user directory
        """
        self.mh_dir = mh_dir
        self.data_dir = os.path.join(self.mh_dir, "data")
        self.model_dir = os.path.join(self.mh_dir, "models")
        self.clothes_dir = os.path.join(self.data_dir, "clothes")
        self.poses_dir = os.path.join(self.data_dir, "poses")
        self.expr_dir = os.path.join(self.data_dir, "expressions")
        self.hair_dir = os.path.join(self.data_dir, "hair")
        self.shoes_dir = os.path.join(self.clothes_dir, "shoes")

        self.model = None
        self.gender = None
        self.age = None
        self.race = None
        self._choose_model()

        self.hair = None
        self._choose_hair()

        self.shoes = None
        self._choose_shoes()

        self.clothes = None
        self._choose_clothes()

        self.pose = None
        self._choose_pose()

        self.expr = None
        self._choose_expression()

    def _choose_model(self):
        """
        Choosing a model file randomly. This function expects 
        the model's age, gender, ethnicity to be encoded in the filename.
        :return:
        """
        model_files = [f for f in os.listdir(self.model_dir) if ".mhm" in f]
        file_name = np.random.choice(model_files)

        self.model = os.path.join(self.model_dir, file_name)

        if "female" in file_name:
            self.gender = "female"
        else:
            self.gender = "male"

        if "young" in file_name:
            self.age = "young"
        elif "old" in file_name:
            self.age = "old"
        else:
            self.age = "middle"

        if "european" in file_name:
            self.race = "european"
        else:
            self.race = "african"

    def __select_cloth_by_gender(self, folder):
        """
        Choosing clothes randomly. Considers gender.
        :param folder: folder where to make a selection
        """
        unisex_folder = os.path.join(folder, "unisex")
        gender_folder = os.path.join(folder, self.gender)

        unisex_files = [os.path.join("unisex", f) for f in os.listdir(unisex_folder)]
        gender_files = [os.path.join(self.gender, f) for f in os.listdir(gender_folder)]

        file = np.random.choice(unisex_files + gender_files)
        cloth_folder = os.path.join(folder, file)

        cloth_file = [f for f in os.listdir(cloth_folder) if ".mhclo" in f][0]
        return os.path.join(cloth_folder, cloth_file)

    def _choose_hair(self):
        """
        Randomly chooses hair
        """
        prob = 1.

        if self.race == "african" and self.gender == "male":
            prob = 0.3

        elif self.race == "european" and self.gender == "male":
            prob = 0.8

        elif self.race == "european" and self.gender == "male" and self.age == "old":
            prob = 0.5

        if np.random.rand() < prob:
            self.hair = self.__select_cloth_by_gender(self.hair_dir)
        else:
            self.hair = None

    def _choose_shoes(self):
        """
        Randomly chooses shoes
        """
        self.shoes = self.__select_cloth_by_gender(self.shoes_dir)

    def _choose_clothes(self):
        """
        Randomly chooses clothes. First, this function randomly decides if a 
        full outfit is chosen or upper and lower body clothes are chosen separately.
        :return:
        """
        p = np.random.rand()
        if p < 0.5:
            folder = os.path.join(self.clothes_dir, "full")
            self.clothes = [self.__select_cloth_by_gender(folder)]
        else:
            folder_upper = os.path.join(self.clothes_dir, "upper")
            folder_lower = os.path.join(self.clothes_dir, "lower")
            file_upper = self.__select_cloth_by_gender(folder_upper)
            file_lower = self.__select_cloth_by_gender(folder_lower)

            self.clothes = [file_lower, file_upper]

    def _choose_expression(self):
        """
        Facial expression gets randomly selected.
        """
        files = [f for f in os.listdir(self.expr_dir) if ".mhpose" in f]
        file = np.random.choice(files)
        self.expr = os.path.join(self.expr_dir, file)

    def _choose_pose(self):
        """
        Pose gets randomly selected
        """
        files = [f for f in os.listdir(self.poses_dir) if ".bvh" in f]
        file = np.random.choice(files)
        self.pose = os.path.join(self.poses_dir, file)

    def get_model(self):
        return self.model

    def get_clothes(self):
        return self.clothes

    def get_hair(self):
        return self.hair

    def get_pose(self):
        return self.pose

    def get_expression(self):
        return self.expr

    def get_shoes(self):
        return self.shoes

    def get_hash(self):
        properties = [self.model, self.clothes, self.hair,
                      self.pose, self.expr, self.shoes]

        json_string = json.dumps(properties, ensure_ascii=False)
        return sha256(json_string.encode('utf-8')).hexdigest()


if __name__ == "__main__":
    import sys

    path = sys.argv[1]

    for i in range(3):
        print(f"-----------------{i}. Random Human -----------------")
        human = RandomHuman(path)
        print(f"Model: {human.get_model()}")
        print("Clothes: ", human.get_clothes())
        print(f"Shoes: {human.get_shoes()}")
        print(f"Pose: {human.get_pose()}")
        print(f"Expression: {human.get_expression()}")
        print(f"Hair: {human.get_hair()}")
        print(f"Hash: {human.get_hash()}")
