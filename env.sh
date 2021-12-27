conda create --name projectenv python=3.9.0
cd /opt/anaconda3/envs/projectenv/lib/python3.9/site-packages
cp /Users/nicolez/Documents/GitHub/LOB-feature-analysis/package/db_lob.cpython-39-x86_64-linux-gnu.so .
cp -r /Users/nicolez/Documents/GitHub/LOB-feature-analysis/package/db_lob-0.0.5.dist-info .
chmod +x db_lob.cpython-39-x86_64-linux-gnu.so

conda install -n projectenv numpy
conda install -n projectenv pandas
conda install -n projectenv scipy
conda install -n projectenv matplotlib
conda install -n projectenv seaborn
conda install -n projectenv sklearn
conda install -n projectenv statsmodels