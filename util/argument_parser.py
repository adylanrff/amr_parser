import argparse
def parse_arguments():
    # Init parser
    parser = argparse.ArgumentParser(description="AMR Parser for Bahasa Indonesia")
    parser.add_argument('--predict', help="Predict mode", action="store_true")
    parser.add_argument('--train', help="Train mode", action="store_true")
    parser.add_argument('--sentence', help="Input sentence", nargs='?')
    parser.add_argument('--file', help="AMR file input path for training or prediction", nargs='?')
    parser.add_argument('--output', help="AMR file output path for saving results", nargs='?', required=True)
    args = parser.parse_args()
    return args