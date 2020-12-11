# MakeHumanGenerator
Plugin to generate random [MakeHuman](http://www.makehumancommunity.org) models. The plugin randomly combines makehuman models, clothing and other assets in your user directory to generate the desired number of models. Each combination is saved as .mhx2 file.
## Folder structure
This plugin expects you to organize your assets in a certain directory structure.
`makehuman/v1py3/data             # data root
  |----clothes/                   # clothes root
  |        |----upper/            # clothes for upper body
  |        |     |---unisex/      # upper body clothes for all genders
  |        |     |---male/        # upper body clothes for males 
  |        |     |---female/      # upper body clothes for females
  |        |----lower/            # same with lower body
  |        |----full/             # same for full body outfits
  |        |----shoes/            # same for shoes
  |----hair/unisex|male|female    # same separation for hair
  |----poses/                     # full body pose
  |----expressions/               # expressions
  `

  The "base models" without any assets must be created in advance and shall indicate age, gender and ethnicity in their name, e. g., `european_male_old.mhm`.

## Usage
Install the plugin as any other MakeHumann plugin and enter the desired parameters (number of models, output folder, T-Pose rig).
