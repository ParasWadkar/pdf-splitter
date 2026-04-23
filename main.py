import argparse
from src.splitter import split_pdf_into_quadrants

def main():
    parser = argparse.ArgumentParser(description="Split PDF pages into 4 parts")
    
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("output", help="Output PDF file")

    args = parser.parse_args()

    split_pdf_into_quadrants(args.input, args.output)
    print(f"✅ Done! Output saved as {args.output}")

if __name__ == "__main__":
    main()