import sys
from util.argument_parser import parse_arguments
args = parse_arguments()

from prediction.predict import predict_from_sentence, predict_from_file

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
