import akshare as ak


def main():
	print('Hi AkShare!')
	for i in range(10):
	    try:
	        data = ak.get_inventory_data(exchange=1, symbol=6, plot=True)
	        print(data)
	        break
	    except:
	        continue
	
if __name__ == '__main__':
	main()