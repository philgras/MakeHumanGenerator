import gui3d
import gui
import os
import json

from .random_human import RandomHuman
from core import G


class GeneratorTaskView(gui3d.TaskView):
    """
    Generator widget which is the interface to
    trigger the generation in makehuman.
    """

    def __init__(self, category):
        """
        Creates the widget with two text inputs to specify the
        number of instances to generate and the output directory
        :param category: where to display the widget
        """
        gui3d.TaskView.__init__(self, category, 'Generator')

        box = self.addLeftWidget(gui.GroupBox('Generator'))

        # number of instances to generate
        self.numberInstances = box.addWidget(gui.TextEdit(text="10"))

        # where to store the generated models
        self.outputTextEdit = box.addWidget(gui.TextEdit(text=os.path.expanduser("~")))

        # progress bars
        self.genProgressBar = box.addWidget(gui.ProgressBar())
        self.genProgressBar.setProgress(0)

        # checkbox to enable occluded face dropping
        self.dropFacesCB = box.addWidget(gui.CheckBox("Drop Occluded Faces"))

        # button to trigger the generation
        self.genButton = box.addWidget(gui.Button('Generate'))

        # used to avoid any duplicate in the current run
        self.duplicate_tracker = {}

        @self.genButton.mhEvent
        def onClicked(event):
            output_dir = self.outputTextEdit.text

            os.makedirs(output_dir, exist_ok=True)
            N = int(self.numberInstances.text)

            self.duplicate_tracker = {}

            for i in range(N):
                name = f"model_{i}"
                path = os.path.join(output_dir, name)
                os.makedirs(path, exist_ok=True)
                self.generateHuman(path)
                self.genProgressBar.setProgress((i + 1) / N)

    def generateHuman(self, folder):
        """
        Generates a random human using the attributes(clothes, hair, etc.)
        obtained from an instance of RandomHuman.
        A preview image is rendered as preview.png the human model 
        is exported as model.mhx2 and the attributes are
        written to attributes.json.
        :param folder: The folder where all the files should be created in.
        """
        mh_dir = os.path.dirname(G.app.mhapi.locations.getUserDataPath())

        while True:
            randomHuman = RandomHuman(mh_dir)
            human_hash = randomHuman.get_hash()

            if human_hash not in self.duplicate_tracker:
                self.duplicate_tracker[human_hash] = None
                break

            print('Found duplicate...')

        G.app._resetHuman()

        # create model in makehuman
        G.app.loadHumanMHM(randomHuman.get_model())
        G.app.mhapi.assets.equipHair(randomHuman.get_hair())
        G.app.mhapi.assets.equipClothes(randomHuman.get_shoes())
        for cloth in randomHuman.get_clothes():
            G.app.mhapi.assets.equipClothes(cloth)

        G.app.mhapi.skeleton.setExpressionFromFile(randomHuman.get_expression())

        # toggle Face hiding
        cloth_handler = G.app.getCategory("Geometries").getTaskByName("Clothes")
        cloth_handler.updateFaceMasks(self.dropFacesCB.selected)
        cloth_handler.faceHidingTggl.setChecked(self.dropFacesCB.selected)

        # Load pose plugin
        pose_plugin = G.app.getPlugin('3_libraries_pose')
        pose_handler = pose_plugin.PoseLibraryTaskView('Pose/Animation')
        pose_handler.loadPose(randomHuman.get_pose())

        G.app.resetView()

        # render thumb nail
        settings = dict()
        settings['scene'] = G.app.scene
        settings['AA'] = True  # Anti Aliasing
        settings['dimensions'] = (800, 600)
        settings['lightmapSSS'] = False
        G.app.getPlugin('4_rendering_opengl').mh2opengl.Render(settings)
        thumb_file = os.path.join(folder, "preview.png")
        gui3d.app.getCategory('Rendering').getTaskByName('Viewer').image.save(thumb_file, iformat="png")

        # create summary json
        base = os.path.basename
        attributes = {}
        if randomHuman.get_hair() is None:
            attributes["hair"] = randomHuman.get_hair()
        else:
            attributes["hair"] = base(randomHuman.get_hair())

        attributes["shoes"] = base(randomHuman.get_shoes())
        attributes["clothes"] = [base(c) for c in randomHuman.get_clothes()]
        attributes["model"] = base(randomHuman.get_model())
        attributes["expression"] = base(randomHuman.get_expression())
        attributes["pose"] = base(randomHuman.get_pose())
        attributes["height"] = gui3d.app.selectedHuman.getHeightCm()
        attributes_file = os.path.join(folder, "attributes.json")
        with open(attributes_file, "w") as f:
            json.dump(attributes, f)

        # set scale units to meter
        for button in G.app.mhapi.exports.getMHX2Exporter().taskview.scaleButtons:
            if "meter" == button[1]:
                print(button[0].setChecked(True))
        # mhx2 export
        mhx2_file = os.path.join(folder, "model.mhx2")
        G.app.mhapi.exports.exportAsMHX2(mhx2_file, useExportsDir=False)
