import argparse
from .doc import doc

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="odpydoc")
    parser.add_argument("target", type=str, help="the target module or package to document")
    args = parser.parse_args()

    doc(args.target)
