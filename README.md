# AMR Parser for Bahasa Indonesia

AMR Parser from dependency parser features. Currently tested in Windows 10, not yet for Ubuntu.
## Getting Started

### Prerequisites

What things you need to install the software and how to install them

```
python 3.9.5 
tensorflow 2.5.0
conda
```

### Installing

To install this app in your device, please do the following instructions

1. ~~Install packages from the *requirements.txt* file~~

```
pip install -r requirements.txt
```
1. As the above method may not work to resolve the requirement dependency, use conda instead, and create new environment from `environment.yml`

```
conda env create -f environment.yml
conda activate amr
```

2. Prepare stanza for Indonesian language support and Tools for evaluation

```
python -c "import stanfordnlp;stanfordnlp.download('id')"
python -c "import stanza;stanza.download('id')"
python -c "import nltk;nltk.download('punkt')"
```

```
git clone https://github.com/ChunchuanLv/amr-evaluation-tool-enhanced tools/amr-eval
```

3. Create `pretrained` directory

4. Download this [zipped_file](https://storage.googleapis.com/riset_amr/adylan/pretrained_feature_models.zip) that contains POS Tagger, NER Tagger, and Word2Vec models and put it in the `pretrained` folder. The tree structure should be like this:

```
pretrained/
    |-pos_tagger/
    |-ner_tagger/
    |-word2vec/

```
4. Create `saved_model` directory

5. Download this pretrained model and encoders from this [link](https://storage.googleapis.com/riset_amr/adylan/pretrained_model_and_encoder.zip) and copy the contents of the file to the `saved_model` directory. The tree structure should be like this.

```
saved_model/
    |-encoder/ 
        |-label_encoder.pickle.dat
        |-one_hot_encoder.pickle.dat
    |-best_model_pretrained.pickle.dat
```


## Running the program

### Prediction

```
python amr_parser --predict --sentence "<any sentence that you want>" --output <filepath>
```

Example:
```
python amr_parser --predict --sentence "Aku makan buah di pagi ini" --output amr.txt
```

The output of the AMR should be included in the `amr.txt` file.

### 

### Training 

COMING SOON

## Authors

* **Adylan Roaffa Ilmy** 
* **Dr. Masayu Leylia Khodra, ST., MT.** - Advisor 


