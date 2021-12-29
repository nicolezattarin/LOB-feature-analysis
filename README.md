# LOB-feature-analysis
upload .csv files [here](https://drive.google.com/drive/folders/1LP0KT5O1YQT1Vf3692nPeoT5SCsrJtUk?usp=sharing)
##  Setup 
### For Linux users
1. Create environment:

    `conda list --explicit > spec-file.txt`
    
    `conda create --name projectenv --file spec-file.txt`

2. Install package: go to `*/anaconda3/envs/projectenv/lib/python3.<version_num>/site-packages` in your file system and paste the .so file and the folder that you can find in `package` folder. 
    For instance:
    
    `cd /opt/anaconda3/envs/projectenv/lib/python3.8/site-packages`
    
    `cp path/package/db_lob.cpython-39-x86_64-linux-gnu.so .`
    
    `cp -r path/package/db_lob-0.0.5.dist-info .`
    
3. Work in the new enviroment:
    `conda activate projectenv`

### For OSX users
Setup a VM with conda and install the package.

Or, for us to work:

* Download a RDP client (from app store [Microsoft Remote Desktop](https://apps.apple.com/it/app/microsoft-remote-desktop/id1295203466?mt=12))
* PC name: 20.108.243.79:3389
* Work in the env with the package intalled: `conda activate project`
* in Jupyter lab use project kernel to run jupyter notebooks, while xsor env works only running python scripts

