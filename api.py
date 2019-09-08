import hug

# put example data that can be overriden
user_json = {
	"userId": "0xBBAac64b4E4499aa40DB238FaA8Ac00BAc50811B",
	"accountBalance": [
		{
			"token": "BNB",
			"amount": "20"
		},
		{
			"token": "BTC",
			"amount": "0.002"
		}
	],
	"shortingProfile": {
		"positions": [
			{
				"id": "1",
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
		]
	},
	"lendingProfile": {
		"applicationBalance": [
			{
				"token": "BNB",
				"amount": "3"
			}
		],
		"projectedBalance": [
			{
				"token": "BNB",
				"amount": "24.34"
			}
		],
		"active": True,
		"lends": [
			{
				"id": "2",
				"principle": "3.0134",
				"ratioLent": "1",
				"expiration": "1568899866",
				"token": "BNB"
			}
		]
	}
}
@hug.cli()
@hug.get(examples='', versions=1)
def profile():
	'''Returns the User JSON.'''
	return user_json



provideLoan_response = {
    "success": True,
    "message": "Lend made available to borrowers"
}
@hug.cli()
@hug.get(examples='userId=1&currency=BNB&amount=10000', versions=1)
def provideLoan(
	userId: hug.types.text,
	currency: hug.types.text,
	amount: hug.types.text
	):
	return provideLoan_response

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
# version 2 will have changeable json with changes that remain only until the server is stopped
# version 3 will use sql to make changes stick
def main():
	profile.interface.cli() 

if __name__ == '__main__':
	main()
