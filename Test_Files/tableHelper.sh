
for dir in ../Test/Reduced/*/
do
    language=$(basename "$dir")
    python makeTableRed.py $language
done