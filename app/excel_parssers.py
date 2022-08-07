# import logging
# from abc import abstractmethod
#
# import openpyxl
#
# from myFinance.models import TransactionNameTag
# from datetime import datetime
# logger = logging.getLogger(__name__)
#
#
# class _ExcelParser:
# 	@abstractmethod
# 	def load_transactions(self, ws, user):
# 		pass
#
# 	@abstractmethod
# 	def is_right_format(self, ws):
# 		pass
#
#
# class CalExcelParser(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in list(ws.iter_rows())[3:-1]:
# 			if not row[1].value or not row[3].value or not row[0].value:
# 				continue
# 			row_data = {}
# 			row_data["name"] = row[1].value
# 			if type(row[3].value) == int or type(row[3].value) == float:
# 				row_data["value"] = row[3].value
# 			else:
# 				row_data["value"] = row[3].value.replace("₪", "").replace(",", "").strip()
# 			row_data["date"] = row[0].value
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		lines = list(ws.iter_rows())
# 		A1 = "פירוט עסקות נכון לתאריך"
# 		A2 = "פירוט עסקות לכרטיס ויזה עסקי"
# 		titels = ["תאריך העסקה", "שם בית העסק", "סכום העסקה", "סכום החיוב", "פירוט נוסף"]
# 		return [x.value for x in lines[2]] == titels
#
#
# class MaxExcelParser(_ExcelParser):
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in list(ws.iter_rows())[4:-1]:
# 			if not row[1].value or not row[5].value or not row[0].value:
# 				continue
# 			row_data = {}
# 			row_data["name"] = row[1].value
# 			row_data["value"] = row[5].value
# 			row_data["date"] = datetime.strptime(row[0].value, '%d-%m-%Y')
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		lines = list(ws.iter_rows())
#
# 		A1 = "פירוט עסקות נכון לתאריך"
# 		A2 = "פירוט עסקות לכרטיס ויזה עסקי"
# 		titels = ['תאריך עסקה',
# 		          'שם בית העסק',
# 		          'קטגוריה',
# 		          '4 ספרות אחרונות של כרטיס האשראי',
# 		          'סוג עסקה',
# 		          'סכום חיוב',
# 		          'מטבע חיוב',
# 		          'סכום עסקה מקורי',
# 		          'מטבע עסקה מקורי',
# 		          'תאריך חיוב',
# 		          'הערות',
# 		          'תיוגים',
# 		          'מועדון הנחות',
# 		          'מפתח דיסקונט',
# 		          'אופן ביצוע ההעסקה',
# 		          'שער המרה ממטבע מקור/התחשבנות לש"ח']
# 		return [x.value for x in lines[3]] == titels
#
#
# class DiscountBankExcelParser(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in list(ws.iter_rows())[13:]:
# 			if not row[0].value or not row[2].value or not row[3].value:
# 				return sorted_transactions + unsorted_transactions
# 			row_data = {}
# 			row_data["name"] = row[2].value
# 			row_data["value"] = -row[3].value
# 			row_data["date"] = row[0].value
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		titels = ['תאריך', 'יום ערך', 'תיאור התנועה', '₪ זכות/חובה ', '₪ יתרה ', 'אסמכתה', 'עמלה', 'ערוץ ביצוע']
# 		lines = list(ws.iter_rows())
# 		return [x.value for x in lines[8]] == titels
#
#
# class FibiBankExcelParser(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in list(ws.iter_rows())[2:]:
# 			if not row[3].value or not row[7].value or (not row[5].value and not not row[6].value):
# 				return sorted_transactions + unsorted_transactions
# 			row_data = {}
# 			row_data["name"] = row[3].value
# 			row_data["value"] = row[6].value if type(row[6].value) != str or row[6].value.strip() else -row[5].value
# 			row_data["date"] = row[7].value
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		titels = ['סוג פעולה', 'תיאור', 'אסמכתא', 'זכות', 'חובה', 'תאריך ערך', 'יתרה']
# 		lines = list(ws.iter_rows())
# 		return [x.value for x in lines[1][2:]] == titels
#
#
# class FibiCredetCaredExcelParser(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in list(ws.iter_rows())[6:]:
# 			if not row[2].value or not row[4].value or not row[1].value:
# 				return sorted_transactions + unsorted_transactions
# 			row_data = {}
# 			row_data["name"] = row[2].value
# 			row_data["value"] = row[4].value
# 			row_data["date"] = row[1].value
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		titels = ['תאריך עסקה', 'שם  העסק', 'סכום עסקה', 'סכום חיוב', 'פירוט']
# 		lines = list(ws.iter_rows())
# 		return [x.value for x in lines[5][1:]] == titels
#
#
# class YhavBankExcelParser(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in list(ws.iter_rows())[6:]:
# 			if not row[3].value or not row[4].value or (not row[1].value and not row[2].value):
# 				return sorted_transactions + unsorted_transactions
# 			row_data = {}
# 			row_data["name"] = row[3].value
# 			row_data["value"] = row[2].value if not row[2].value == '0' else -row[1].value
# 			row_data["date"] = row[6].value
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		titels = ['יתרה משוערכת(₪)', 'זכות(₪)', 'חובה(₪)', 'תיאור פעולה', 'אסמכתא', None, 'תאריך ערך']
# 		lines = list(ws.iter_rows())
# 		return [x.value for x in lines[5][:7]] == titels
#
# class YhavCreditCardExcelParser(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in list(ws.iter_rows())[10:]:
# 			if not row[1].value or not row[8].value or not row[14].value:
# 				continue
# 				# return sorted_transactions + unsorted_transactions
# 			row_data = {}
# 			row_data["name"] = row[8].value
# 			row_data["value"] = row[1].value
# 			row_data["date"] = row[14].value
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		titels = ['מידע נוסף', 'סכום חיוב(₪)', None, 'הצגת כרטיס', None, None, 'מספר זיהוי עיסקה', None, 'תיאור פעולה', None, None, None, None, None, 'תאריך']
# 		lines = list(ws.iter_rows())
# 		return [x.value for x in lines[9][:15]] == titels
#
#
# class PoalimBankExcelParser(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in list(ws.iter_rows())[6:]:
# 			if not row[0].value or not row[1].value or not (row[4].value or row[5].value):
# 				continue
# 				# return sorted_transactions + unsorted_transactions
# 			row_data = {}
# 			row_data["name"] = row[1].value
# 			row_data["value"] = row[4].value if row[4].value and row[4].value != '' else -row[5].value
# 			row_data["date"] = row[0].value
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		titels = ['תאריך', 'הפעולה', 'פרטים', 'אסמכתא', 'חובה', 'זכות', "יתרה בש''ח", 'תאריך ערך', 'לטובת', 'עבור']
# 		lines = list(ws.iter_rows())
# 		return [x.value for x in lines[5]] == titels
#
# class IsracardDirectExcelParser(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		foren_transactions = False
#
# 		for row in list(ws.iter_rows())[6:]:
# 			if row[0] and row[0].value == 'עסקאות בחו˝ל':
# 				foren_transactions= True
# 			if not foren_transactions:
# 				if not row[0].value or not row[1].value or not row[4].value or not isinstance(row[4].value, (int, float)):
# 					continue
# 					# return sorted_transactions + unsorted_transactions
# 				row_data = {}
# 				row_data["name"] = row[1].value
# 				row_data["value"] = row[4].value
# 				row_data["date"] = row[0].value
# 				tag = TransactionNameTag.get_tag(row_data["name"], user)
# 				if tag:
# 					row_data["tag"] = tag.name
# 					sorted_transactions.append(row_data)
# 				else:
# 					unsorted_transactions.append(row_data)
# 			else:
# 				if not row[0].value or not row[2].value or not row[5].value or not isinstance(row[5].value, (int, float)):
# 					continue
# 					# return sorted_transactions + unsorted_transactions
# 				row_data = {}
# 				row_data["name"] = row[2].value
# 				row_data["value"] = row[5].value
# 				row_data["date"] = row[0].value
# 				tag = TransactionNameTag.get_tag(row_data["name"], user)
# 				if tag:
# 					row_data["tag"] = tag.name
# 					sorted_transactions.append(row_data)
# 				else:
# 					unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		titels = ['תאריך רכישה', 'שם בית עסק', 'סכום עסקה', 'מטבע מקור', 'סכום חיוב', 'מטבע לחיוב', 'מספר שובר', 'פירוט נוסף']
# 		lines = list(ws.iter_rows())
# 		return [x.value for x in lines[5]] == titels
#
#
# def load_excel_file(ws, user):
# 	sorted_transactions = list()
# 	unsorted_transactions = list()
# 	# iterating over the rows and
# 	# getting value from each cell in row
# 	for row in list(ws.iter_rows()):
# 		if not row[1].value or not row[3].value or not row[0].value:
# 			continue
# 		row_data = {}
# 		row_data["name"] = row[1].value
# 		row_data["value"] = row[3].value.replace("₪", "").replace(",", "").strip()
# 		row_data["date"] = row[0].value
# 		tag = TransactionNameTag.get_tag(row_data["name"], user)
# 		if tag:
# 			row_data["tag"] = tag.name
# 			sorted_transactions.append(row_data)
# 		else:
# 			unsorted_transactions.append(row_data)
# 	return sorted_transactions + unsorted_transactions
#
#
# class BenLeumiBankExcelParser(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in list(ws.iter_rows())[3:]:
# 			if not row[3].value or not row[1].value or not (row[5].value or row[6].value):
# 				continue
# 				# return sorted_transactions + unsorted_transactions
# 			row_data = {}
# 			row_data["name"] = row[3].value
# 			row_data["value"] = -row[5].value if row[5].value and row[5].value != '' and row[5].value != ' ' else row[6].value
# 			row_data["date"] = row[1].value
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		titels = ['סוג פעולה', 'תיאור', 'אסמכתא', 'זכות', 'חובה', 'תאריך ערך', 'יתרה']
# 		lines = list(ws.iter_rows())
# 		return [x.value for x in lines[1][2:9]] == titels
#
#
# class BenLeumiBankExcelParser1(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in list(ws.iter_rows())[4:]:
# 			if not row[3].value or not row[1].value or not (row[5].value or row[6].value):
# 				continue
# 				# return sorted_transactions + unsorted_transactions
# 			row_data = {}
# 			row_data["name"] = row[5].value
# 			row_data["value"] = -row[3].value if row[3].value and row[3].value != '' and row[3].value != ' ' else row[4].value
# 			row_data["date"] = row[8].value
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		titels = ['תאריך ערך', 'זכות', 'חובה', 'תאור', 'אסמכתא', 'סוג פעולה', 'תאריך']
# 		lines = list(ws.iter_rows())
# 		return [x.value for x in lines[1][2:9]] == titels
#
# class BanckDiscountLoader(_ExcelParser):
#
# 	def load_transactions(self, ws, user):
# 		sorted_transactions = list()
# 		unsorted_transactions = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in ws:
#
# 			row_data = {}
# 			row_data["name"] = None
# 			row_data["value"] =None
# 			row_data["date"] = None
# 			tag = TransactionNameTag.get_tag(row_data["name"], user)
# 			if tag:
# 				row_data["tag"] = tag.name
# 				sorted_transactions.append(row_data)
# 			else:
# 				unsorted_transactions.append(row_data)
# 		return sorted_transactions + unsorted_transactions
#
# 	def is_right_format(self, ws):
# 		return type(ws) == list
#
# class ExcelParser:
# 	parsers = [BanckDiscountLoader(),BenLeumiBankExcelParser1(), BenLeumiBankExcelParser(), IsracardDirectExcelParser(), PoalimBankExcelParser(), YhavCreditCardExcelParser(), YhavBankExcelParser(), FibiCredetCaredExcelParser(), FibiBankExcelParser(), CalExcelParser(),
# 	           MaxExcelParser(),
# 	           DiscountBankExcelParser()]
#
# 	def parse_excel(self, excel_file, user):
# 		wb = openpyxl.load_workbook(excel_file)
# 		worksheet = wb.worksheets[0]
# 		for parser in self.parsers:
# 			try:
# 				if parser.is_right_format(worksheet):
# 					return parser.load_transactions(worksheet, user)
# 			except Exception as e:
# 				logger.exception(str(e))
# 				pass
# 		return None
