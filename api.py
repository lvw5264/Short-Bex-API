import hug
from datetime import datetime, timedelta
import random

INTEREST = 0.07 # set all interest to 7%
EXPIRY_DAYS = 60 # set all expiry date to 60 days in the future

# The database stand in, with one example
lends = {
	"5738": { # for now UUID is 4 digit rand
		"lenderId": "0xe35063492beD79a917Ad10D1Aa54530451CfD13c",
		"principal": "3.0134",
		"ratioLent": "1",
		"expiration": "1568899866",
		"token": "BNB",
		"applicationBalance": { # amount currently in
			"BNB": {
				"amount": "3"
			}
		}
	}
}
positions = {
	"5421": { # for now UUID is 4 digit rand
		"shorterId": "0xBBAac64b4E4499aa40DB238FaA8Ac00BAc50811B",
		"loanId": "5738",
		"isOpen": True,
		"collateral": "1",
		"principle": "3.0134",
		"token": "BNB",
		"openPrice": "22.00",
		"currentPrice": "20.00",
		"terminationPrice": "44.00",
		"interestAccumlated": "0.001",
		"expiration": "1568899866"
	}
}
users = {
	"0xe35063492beD79a917Ad10D1Aa54530451CfD13c": {  # a lender
		"accountBalance": { # personal balance out of our control
			"BNB": {
				"amount": "200"
			},
			"BTC": {
				"amount": "250"
			}
		},
		"availableBalance": { # escrow balance
			"BNB": {
				"amount": "0"
			},
			"BTC": {
				"amount": "0"
			}
		},
		"isShorter": False,
		"isLending": True
	},
	"0xBBAac64b4E4499aa40DB238FaA8Ac00BAc50811B": {  # a shorter
		"accountBalance": { # personal balance out of our control
			"BNB": {
				"amount": "20"
			},
			"BTC": {
				"amount": "0.002"
			}
		},
		"availableBalance": { # escrow balance
			"BNB": {
				"amount": "0"
			},
			"BTC": {
				"amount": "0"
			}
		},
		"isShorter": True,
		"isLending": False
	}
}

@hug.post(versions=2, examples='userId=0xBBAac64b4E4499aa40DB238FaA8Ac00BAc50811B&isShorter=True&isLending=False')
def createUser(userId: hug.types.text, isShorter: hug.types.boolean, isLender: hug.types.boolean):
	# create the user
	user = {}
	user['accountBalance'] = {} # will store account accountBalance objects per token, in the future will populate from blockchain
	user['availableBalance'] = {} # stores escrow balance under our control
	user['isShorter'] = isShorter
	user['isLending'] = isLending # set to false to stop lending

	# add user to the database
	users[userId] = user
	
	return user


@hug.get(examples='userId=0xBBAac64b4E4499aa40DB238FaA8Ac00BAc50811B', versions=2)
def profile(userId: hug.types.text):
	'''Returns the User JSON.'''
	try:
		return users[userId]
	except KeyError: # userId not found
		return {}



# replace with actual blockchain transaction later, but centralized db exchange for now
def send(sender_account, recipient_account, token, amount):
	try: # check if sender has a token balance
		sender_token = sender_account[token]

	except KeyError:
		return False
	
	try: # check if recipient has a token balance, initialize to 0 if not found
		recipient_token = recipient_account[token]
	except KeyError:
		recipient[token] = {
			"amount": 0
		}
	
	if int(sender_account[token]['amount']) <= int(amount): # also counts 0 and negative amount
		# actually exchange values
		sender_account[token]['amount'] = str(int(sender_account[token]['amount']) - int(amount))
		recipient_account[token]['amount'] = str(int(recipient_account[token]['amount']) + int(amount))
		return True
	else:
		return False

@hug.post(examples='lenderId=0xe35063492beD79a917Ad10D1Aa54530451CfD13c&token=BNB&loanAmount=200', versions=2)
def lenderDeposit(
	lenderId: hug.types.text,
	token: hug.types.text,
	loanAmount: hug.types.text
	):

	# check the loanAmount, only positive accepted
	if int(loanAmount) <= 0:
		return {
			"success": False,
			"message": "loanAmount %s must be higher than 0 and not negative." % loanAmount
		}
	
	# find the first lenderId
	try:
		lender = users[lenderId]

	except KeyError:
		return {
			"success": False,
			"message": "No lender userId: %s was found, nothing was lent." % lenderId
		}

	# actually send amounts from lenderProfile/accountBalance to lenderProfile/availableBalance, which is the escrow on our server outside their control
	if send(lender['accountBalance'], lender['availableBalance'], token, loanAmount):
		return {
			"success": True,
			"message": "Lender userId: %s successfully deposited %s of token %s in system escrow." % (lenderId, loanAmount, token)
		}
	else:
		return {
			"success": False,
			"message": "Lender userId: %s has insufficient funds %s of token %s to deposit in system escrow." % (lenderId, loanAmount, token)
		}

closeLoan_response = {
	"success": True,
	"message": "Fund withdraw initiated, please await remaining lenders to return funds for at most 2 months"
}
@hug.cli()
@hug.get(examples='loanId=1', versions=1)
def closeLoan(loanId: hug.types.text):
	return closeLoan_response


openPosition_response = {
	"success": True,
	"message": "Position opened"
}

@hug.cli()
@hug.get(examples='collateral=10000&principal=10000&currency=BNB', versions=1)
def openPosition(
	collateral: hug.types.text,
	principal: hug.types.text,
	currency: hug.types.text
	):
	return openPosition_response



# create a lend smart contract for each specific lender
def lend(borrower, lender, token, principal, interest):
	if send(lender['availableBalance'], borrower['accountBalance'], token, loanAmount):
		return {
			"success": True,
			"message": "Lender userId: %s successfully deposited %s of token %s to borrower: %s." % (lenderId, principal, token)
		}
	else:
		return {
			"success": False,
			"message": "Lender userId: %s has insufficient funds %s of token %s to provide to borrower" % (lenderId, principal, token)
		}

@hug.get(examples='borrowerId=0xBBAac64b4E4499aa40DB238FaA8Ac00BAc50811B&collateral=10000&principal=10000&token=BNB', versions=3)
def openPosition(
	borrowerId: hug.types.text,
	collateral: hug.types.text,
	principal: hug.types.text,
	token: hug.types.text
	):
	
	# check if borrower exists
	try:
		borrower = users[borrower_id]
	except KeyError:
		return {
			"success": False,
			"message": "Borrower user_id %s not found." % borrower_id
		}
	
	# Query sum of escrow funds from every user available to be borrowed for this token
	availableTotal = 0
	for user in users:
		try:
			availableAmount = int(user['availableBalance'][token]['amount'])
			if availableAmount > 0:
				availableTotal += availableAmount
				
		except KeyError: # skip user if token not available
			pass
	
	# Compare sum of available escrow funds to the principal
	if availableTotal == 0:
		return {
			"success": False,
			"message": "No liquidity is available for %s token." % token
		}
	# If principal exceeds available escrow, end and return an error message to the user "Not enough liquidity available for trade"
	elif int(principal) > availableTotal:
		return {
			"success": False,
			"message": "Not enough liquidity, only %s of %s token available for trade: lower the principal or try again later." % (availableTotal, token)
		}
	# If principal is less than or equal to sum of available escrow, enough funds are available for the margin trade.
	else:
		# Store a deadline timestamp as 60 days from now
		expiration = datetime.now() + timedelta(days=EXPIRY_DAYS)
		
		# match start matching requested principal with escrow from each user (does not handle concurrency, must be serial!)
		lenders = []
		for user in users:
			# For each user queried, check if their lending status is set to available for lending
			if user['isLending']:
				# If available, check if their funds fully cover the principal (are equal).
				if principal == availableTotal:
					# If they do, stop here, store lender ratio to 1 as well as lender address (the lender ID) as the only element in the lenders array for the position, convert principle to USD, store USD in position
					lenders.append(user)
					
					# actually lend money
					lend(borrower, user, token, principal, INTEREST)
			# If not available, skip.
		
		return {
			"success": True,
			"message": "Position opened: %s of %s token, expires %s" % (principal, token, expiration)
		}


closePosition_response = {
	"success": True,
	"message": "Close complete",
	"difference": "-20"
}

@hug.cli()
@hug.get(examples='userId=1&positionId=1', versions=1)
def closePosition(
	userId: hug.types.text,
	positionId: hug.types.text
	):
	return closePosition_response

# version 1 will only return immutable json
# version 2 and forward will have changeable json with changes that remain only until the server is stopped
# version 2 will allow profile, lenderDeposit functions
# version 3 will allow openPosition,closePosition, closeLoan
# version 5 will use sql to make changes stick
