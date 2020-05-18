# AMR Parser for Bahasa Indonesia

AMR Parser from dependency parser features

## Getting Started

### Prerequisites

What things you need to install the software and how to install them

```
python3 
tensorflow
```

### Installing

To install this app in your device, please do the following instructions

1. Install packages from the *requirements.txt* file

```
pip install -r requirements.txt
```

2. Create `pretrained` directory

3. Download this [zipped_file](https://drive.google.com/file/d/1-aOwaGox1GSEbdcCDl683pV4M3-HQJG6/view?usp=sharing) that contains POS Tagger, NER Tagger, and Word2Vec models and put it in the `pretrained` folder. The tree structure should be like this:

```
pos_tagger/
ner_tagger/
word2vec/

```
4. Create `saved_model` directory

5. Download this pretrained model and encoders from this [link](https://drive.google.com/file/d/1J0HPnVe12DFDgmq886YlbDDlveQp1l7a/view?usp=sharing) and copy the contents of the file to the `saved_model` directory. The tree structure should be like this.

```
encoder/ 
---label_encoder.pickle.dat
---one_hot_encoder.pickle.dat
best_model_pretrained.pickle.dat
```


## Running the program

### Prediction

```
python3 amr_parser --predict --sentence <any sentence that you want> --output <filepath>
```

Example:
```
python3 amr_parser --predict --sentence "Aku makan buah di pagi ini" --output amr.txt
```

The output of the AMR should be included in the `amr.txt` file.

### Training 

COMING SOON

## Authors

* **Adylan Roaffa Ilmy** 
* **Dr. Masayu Leylia Khodra, ST., MT.** - Advisor 


