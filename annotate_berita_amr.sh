cat data/corpus\ berita/topics.txt | while read topic
do 
    ls data/corpus\ berita/sentence/train/docs/$topic/ --width=1 | while read filename 
    do
        python3 amr_parser.py --predict --file data/corpus\ berita/sentence/train/docs/$topic/$filename --output data/corpus\ berita/amr/$topic/$filename.amr
    done
done
