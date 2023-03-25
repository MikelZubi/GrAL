#eval "$(conda shell.bash hook)"
#conda activate ~/a2t_env

#source ~/inguruneak/GrAL/bin/activate

source ~/inguruneak/transformers-4.6.0/bin/activate


echo "Test-ak ejekutatzen"

python test.py
python testAll.py
python testCross.py

echo "Bukatuta"