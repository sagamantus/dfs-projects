import argparse

ap = argparse.ArgumentParser(description="Maze Solver")
ap.add_argument("-i", "--input", required=True, help="Maze input file")
ap.add_argument("-o", "--output", required=False, default="output.txt", help="Solved Maze output file")

args = ap.parse_args()