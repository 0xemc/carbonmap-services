import argparse

def get_file_arg():
    # Create the parser
    parser = argparse.ArgumentParser(description='Process an image file.')
    parser.add_argument('ImagePath', metavar='path', type=str, help='the path to an image file')
    # Parse the arguments
    args = parser.parse_args()

