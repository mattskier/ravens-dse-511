import pandas as pd 
import numpy as np 
from financial_data import *
from misc import *

def main():
	# data = load_original_dataset()
	clean_data = load_clean_dataset()
	print(clean_data[0].head())


if __name__ == '__main__':
	main()