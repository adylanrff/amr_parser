import sys
from util.argument_parser import parse_arguments
import warnings
warnings.filterwarnings("ignore")

args = parse_arguments()

from prediction.predict import predict_from_sentence, predict_from_file
from training.train import train

if __name__ == "__main__":
    filepath = args.file
    output_path = args.output
    if args.predict:
        sentence = args.sentence
        if sentence is not None and filepath is not None:
            print("Choose either to predict a sentence or a file")
            sys.exit(1)
        elif sentence is not None:
            predict_from_sentence(sentence, output_path)
        else:
            predict_from_file(filepath, output_path)

    if args.train:
        if filepath is None:
            print("Specify training data filepath")
            sys.exit(1)
        else:
            train(filepath)