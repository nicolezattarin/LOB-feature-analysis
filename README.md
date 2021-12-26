# LOB-feature-analysis

## Setup
1. Create environment:
    `conda list --explicit > spec-file.txt`

    `conda create --name projectenv --prefix ./envs --file spec-file.txt`

2. Install package: go to `*/anaconda3/envs/projectenv/lib/python3.<version_num>/site-packages` in your file system and paste both db_lob-0.0.4.dist-info and db_lob.cpython-39-x86_64-linux-gnu.so inside site-packages folder. 
    For instance:
    `cd /opt/anaconda3/envs/projectenv/lib/python3.8/site-packages`
    `cp /Users/nicolez/Documents/GitHub/LOB-feature-analysis/package/db_lob.cpython-39-x86_64-linux-gnu.so .`
    `cp -r /Users/nicolez/Documents/GitHub/LOB-feature-analysis/package/db_lob-0.0.5.dist-info .`
    `chmod +x db_lob.cpython-39-x86_64-linux-gnu.so` 

3. Work in the new enviroment:
    `conda activate projectenv`
    `conda deactivate`

