from urllib2 import Request, urlopen, URLError
from collections import namedtuple
import json


url = 'https://api.koleimports.com/products'
columns = ['sku', 'upc', 'title', 'description', 'p_type', 'brand', 'colors', 'materials', 'attributes', 'tags', 'category_id', 'unit_weight', 'category', 'subcategory_id', 'subcategory', 'inventory', 'created', 'modified', 'image_url', 'supplier_id']
priceColumns = ['quantity','price']

price_id = 1
end = False
newUrl = url
text_file = open('koleproductssql.txt', 'w')

def get25Products( url ):
	request = Request(url)
	authorizationToken = 'Basic WDUzNjU1OmYwZjE1MjdkMzdjMzQxYTVlNzc0NWZmMjQwNGQzZTVhNTY3YjAxZDU='
	request.add_header('Authorization', authorizationToken)
	request.add_header('Accept', 'application/vnd.koleimports.ds.product+json')

	try:
		response = urlopen(request)
		productsResponse = response.read()
		productsJson = json.loads(productsResponse)
		parseResponseToFile(productsJson)
	except URLError, e:
	    print 'Got an error code:', e
	    end = True

	return;

def parseResponseToFile( response ):
	products = response['products']
	print('converting 25 products to sql')

	for key, value in products.iteritems():

		if key != 'links':
			print('parsing product with key ' + key)
			text_file.write('INSERT INTO "CheapHerder_product" (')
			str = ''
			for elem in columns:
				if str != '':
					str = str + ', ' + elem
				else:
					str = elem

			str = str + ')'
			text_file.write(str)

			valueStr = getValues(value)
			text_file.write(' values (' + valueStr + ');')
			text_file.write('\n')
			text_file.write(getPricesForProduct(value))
			print('product written to file')
		else:
			global newUrl
			index = next(index for (index, d) in enumerate(value) if d["method"] == "listNextProducts")
			newUrl = value[index]["url"].replace('amp;','')

def getValues( value ):
	valueStr = ''
	for elem in columns:
			if elem == 'image_url':
				val = value['images']
				count = len(val)
				if count != 0:
					imageDict = val[count-1]
					url = imageDict['url']
					urlVal = '\'' + url + '\''
					valueStr = concatenateValueStr(valueStr, urlVal)
				else:
					valueStr = concatenateValueStr(valueStr, '')

			elif elem == 'supplier_id':
				valueStr = concatenateValueStr(valueStr, '1')
			elif elem == 'p_type':
				val = value['type']
				if val is None:
					valueStr = concatenateValueStr(valueStr, '')
				elif isinstance(val, ( int, long )):
					valueStr = concatenateValueStr(valueStr, str(value[elem]))
				elif isinstance(val, ( float )):
					valueStr = concatenateValueStr(valueStr, str(value[elem]))
				else:
					stringVal = '\'' + val + '\''
				   	valueStr = concatenateValueStr(valueStr, stringVal)
			else:
				val = value[elem]
				if val is None:
					valueStr = concatenateValueStr(valueStr, '\'\'')
				elif isinstance(val, ( int, long )):
					valueStr = concatenateValueStr(valueStr, str(value[elem]))
				elif isinstance(val, ( float )):
					valueStr = concatenateValueStr(valueStr, str(value[elem]))
				else:
					stringVal = '\'' + val + '\''
				   	valueStr = concatenateValueStr(valueStr, stringVal)



	return valueStr
def concatenateValueStr(valueStr, str):
	if valueStr != '':
		return valueStr + ', ' + str
	else:
		return str

def getPricesForProduct( product ):
	priceVal = product['tiers']
	prices = ''
	for key, value in priceVal.iteritems():
		if key != 'case':
			quantity = value['quantity']
			price = value['price']
			global price_id

			priceQuery = 'INSERT INTO "CheapHerder_price" ( price_id, quantity, price ) values ( ' + str(price_id) + ', ' + str(quantity) + ', ' + str(price) + ' );\n'
			productPriceQuery = 'INSERT INTO "CheapHerder_product_price" ( sku_id, price_id_id ) values ( ' + '\'' + str(product['sku']) + '\'' + ', ' + str(price_id) + ' );\n'
			price_id = price_id + 1
			prices = prices + priceQuery + productPriceQuery
	return prices

print('start parsing products...')
i = 0
while (end==False):
	print('the new url is ' + newUrl)
	get25Products(newUrl)
	i = i + 1

text_file.close()
print('donee!!!')
print('finished with ' + str(i*25) + 'products')
