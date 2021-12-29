# LOB-feature-analysis
Upload .csv files [here](https://drive.google.com/drive/folders/1LP0KT5O1YQT1Vf3692nPeoT5SCsrJtUk?usp=sharing)

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

## Main changes history
* Zatta 29/12: the file `clean_data.py` is meant to be run on the VM, see its documentation in the file itself. The idea is to to create df from book objects and to save data in .csv files, in such a way that we can work on our own devices without using the VM. I'm not sure if the messages are loaded in chronological order, so the meaning of the data stored in  `data_cleaned/spread.csv` is probably not 100% correct. Data cannot be uploaded on github, thus if you create files with a large amount of data upload them [here](https://drive.google.com/drive/folders/1LP0KT5O1YQT1Vf3692nPeoT5SCsrJtUk?usp=sharing). 
