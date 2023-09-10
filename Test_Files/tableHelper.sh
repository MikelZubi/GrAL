for dir in Test/Reduced3/*/
do
    language=$(basename "$dir")
    python makeTableRed3.py $language
done