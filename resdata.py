import requests
import json
from datetime import datetime, date 
from decimal import Decimal
import mysql.connector
try:
    #Establish connection to the MySQL server
    connection = mysql.connector.connect(
        host="localhost",
        user="test",
        password="password@12",
        database="aloo"
    )
    #Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    def get_bank_statement(email):
        #print("getting the account number of the user")
            #Retrieve the account number based on the email ID
        query = "SELECT account_number FROM account_information WHERE email_id = %s"
        query1 = "SELECT * FROM account_information WHERE email_id = %s"
        # print(query)
        cursor.execute(query, (email,))
        account_number = cursor.fetchone()[0]

        cursor.execute(query1, (email,))
        data = cursor.fetchone()[0]
        #print(data)
        #print(account_number)
        return account_number
            # Retrieve the bank statement for the specified period
            # query = "SELECT * FROM account_statement WHERE account_number = %s AND start_date >= %s AND end_date <= %s"
            # cursor.execute(query, (account_number, start_date, end_date))
            # bank_statement = cursor.fetchall()

            #  Print the bank statement
            # print("Bank Statement from {} to {}:".format(start_date, end_date))
            # for transaction in bank_statement:
            #     print(transaction)

            #  Query to fetch the last five transactions
            # cursor.execute("SELECT * FROM account_statement WHERE account_number = %s ORDER BY transaction_id DESC LIMIT 5", (account_number,))
            # last_five_transactions = cursor.fetchall()

            # Print the last five transactions
            # print("\nLast Five Transactions:")
            # for transaction in last_five_transactions:
            #     print(transaction)   
    # Example usage:
    email = "bob@example.com"
    get_bank_statement(email)

    API_URL = 'http://ec2-13-201-130-252.ap-south-1.compute.amazonaws.com:8080/v1chat/prompt'
    # input_mail = input("")
    input_mail = '''
    what is my account statement from jan 2023
    
    '''
    print("\n=====================input mail========================\n", input_mail)
    data = {
    "messages": [
        {
        "content": '''
        You are designed to answer queries received from bank users. Please classify the question asked into intent described below. Give answer in one word. I need intent only in one word, I am using your output to use a switch case: 
        classify the mail into below 4 categories. Do not provide any extra explanation.
        AccountStatement = balance statement for account
        loanDue = Regarding the loan amount.
        genQuery = if user is asking general questions related to banking, not specific about any user account or user specific services.
        Complaints = categorise user conplaints in this category. 
        If more than one query is asked give answer in a list.
        Do not overthink or assume the intent behind the message other than what is directly described in the message. Do not justify yourself. I am using your output in my code, just give one word answer.
        Do not assume any other category. If the message strictly belongs to above categories, then only categorize that. If you are not sure. Please categorize as NotAvailable and do not provide any other explanation when message comes under NotAvailable category.
        Do not assume fund transfer as loan payment, it can be any other type of fund transfer, just give output as "NotAvailable"  only, no other explanation.
        ''',
        "role": "system"
        },
        {
        "content": input_mail,
        "role": "user"
        }
    ]
    }
    # Make a POST request to the API endpoint with the data
    response = requests.post(API_URL, json=data)
    # Check the response from the API
    if response.status_code == 200:
        # API call successful
        api_response = response.json()
        #print('API Response:', api_response)

        content = api_response['choices'][0]['message']['content']
        #print('Content:', content)
        def email_generation(context):
            # account = account_statement()
            prompt = '''
                    You are an AI system named AUMitra designed to analyse incoming customer emails for AU Small Finance Bank and generate concise, genuine responses. Your goal is to understand the customer's query or concern and provide a helpful and appropriate response. Your responses should be clear, courteous, and to the point.
                    please consider all the points described below and generate polite, short and crisp email using the below points:
                        Analyse the Email.
                        Understand Customer Intent.
                        Address Specific Points.
                        Use Empathetic Language.
                        Provide Genuine Assistance.
                        Conclude Professionally.
                         
                    consider all types of messages to be a mail.
                '''
            prompt += f"\nUse context information provided below.\n {context}"
            data = {
            "messages": [
            {
                "content": prompt,
                "role": "system"
                },
                {
                "content": input_mail,
                "role": "user"
                }
            ]
            }
            # Make a POST request to the API endpoint with the data
            response = requests.post(API_URL, json=data)
            # Check the response from the API
            if response.status_code == 200:
            # API call successful
                api_response = response.json()
                #print('API Response:', api_response)
                generated_mail = api_response['choices'][0]['message']['content']
                print('\n ================================generated mail response==================================\n', generated_mail)
                return generated_mail
            else:
            # API call failed
                print('API Error:', response.status_code, response.text) 
                return ""       
        def account_statement():
            transaction1 = []
            # email_res = email_generation()
            # email_response = str(email_res)
            # print(type(email_response))
            # print(email_response)
            #print("email id:", email)
            account_number = get_bank_statement(email) 
            #print(account_number)
            #print("account statement call made")
            data = {
            "messages": [
            {
            "content": '''
                You are designed to get data from emails received from user for a bank. 
                I want specific keywords from the message as described below. Just answer in the format described below, nothing else.
    
                if user asking to fetch account statement, then give start date and end date from the message  exactly in below format: just give string given below
                            {"accountStatemtent":{"startDate": "yyyy-mm-dd","endDate": "yyyy-mm-dd"}}
                if any of the date is not available return null in respective date, and for present date return 'present' in date.
    
                if user is asking regarding its account balance details, give output in the format below:
                            {"accountBalance":{}}
    
    
                if user is asking its account details regarding account information, example  account number, registered name, IFSC code etc., give information in below format: 
                            {"account_information":{'whatever is asking' : {}}}
    
                If user is asking for anything else other than the categories above. give response in below format:
                            {"unavailable":{}}
                Do not overthink or assume the information behind the message other than what is directly described in the message. Do not justify yourself. I am using your output in my code.
                Do not assume any other category. If the message strictly belongs to above categories, then only categorize that. If you are not sure. Please categorize as unavailable and do not provide any other explanation when message comes under unavailable category.
            ''',
            "role": "system"
            },
            {
            "content": input_mail,
            "role": "user"
            }
            ]
            }
            # Make a POST request to the API endpoint with the data
            response = requests.post(API_URL, json=data)
            # Check the response from the API
            if response.status_code == 200:
            # API call successful
                api_response = response.json()
                #print('API Response:', api_response)
                content = api_response['choices'][0]['message']['content']
                # contentJson = json.loads(content)["accountStatement"]
                # endDate  = contentJson["endDate"]
                # if endDate == 'present':
                #     endDate = datetime.now().date()
                # if endDate == 'present':
                #     endDate = datetime.now().date()
                # #  data = json.loads(content1)
                # #  account_statement = data.get('account_statement', {})
                #print('Content:', content)
                #print(content)
                data_dict = json.loads(content)
                # Extract the key
                key = list(data_dict.keys())[0]
                #print(key)
                #print("the information of the customer account")    
                if key == 'accountBalance':
                    query = f"select running_balance from account_statement WHERE account_number = {account_number}"
                    cursor.execute(query)
                    account_balance = cursor.fetchone()
                    account_balance = float(account_balance[0])
                    # print("the running account balance is:",account_balance)
                    return account_balance, f"your account balance is {account_balance}"
                    #print(endDate)
                # Retrieve the bank statement for the specified period
                #query = f"SELECT * FROM account_statement WHERE account_number = %s AND start_date >= %s AND end_date <= %s"
                #print("jdfdjfjdfjjf", account_number)
                #query = f"SELECT * FROM account_statement WHERE account_number = {account_number}"
                #print("QUERY", query)
                # cursor.execute(query, (account_number, contentJson["startDate"], endDate))
                elif key == 'accountStatement':
                    # contentJson = json.loads(content)["accountStatement"]
                    # endDate  = contentJson["endDate"]
                    # if endDate == 'present':
                    #     endDate = datetime.now().date()
                    # if endDate == 'present':
                    #     endDate = datetime.now().date()
                    contentJson = json.loads(content)["accountStatement"]
                    endDate  = contentJson["endDate"]
                    if endDate == 'present':
                        endDate = datetime.now().date()
                    if endDate == 'present':
                        endDate = datetime.now().date()
                    #  data = json.loads(content1)
                    #  account_statement = data.get('account_statement', {})
                    query = f"select * from account_statement WHERE account_number = {account_number}"
                    cursor.execute(query)
                    bank_statement = cursor.fetchone()
                    #print(bank_statement)
                    if bank_statement:
                    # Assuming the order of columns in the table matches the order of attributes you mentioned
                        attributes = [
                            "transaction_id",
                            "account_number",
                            "description",
                            "transaction_type",
                            "transaction_amount",
                            "running_balance",
                            "total_credits",
                            "total_debits",
                            "closing_balance",
                            "start_date",
                            "end_date"
                        ]
            
                    #return attribute
                    #print(type(attribute))
                    #Print the bank statement
                    bank_statement1 = "Bank Statement from {} to {}:".format(contentJson["startDate"], endDate)
                    #print(bank_statement1)

                    for attribute, value in zip(attributes, bank_statement):
                        if isinstance(value, Decimal):
                            value = float(value)
                        elif type(value) is date:
                            value = value.strftime('%Y-%m-%d')
                        transaction1.append({attribute:value})
                        #print("the account statement of the customer is:",transaction1)
                
                    #print(f"{attribute}: {value}")
                #print(transaction1)
                # print("the account statement of the customer is:",transaction1)
                # for transaction in bank_statement:
                #     transaction1.append(transaction)
                #print(type(transaction1))
                    transactionn = ", ".join(str(item) for item in transaction1)
                #print("=================================================================")
                #print(transactionn)
                    # print(type(email_response))
                    # final_output = email_response + "\n" + bank_statement1 + "\n" + transactionn
                    # print("the final output is :\n",final_output)
                    # print(transactionn)
                    return transactionn, f"your transaction details are below \n {transactionn}"
            # Query to fetch the last five transactions
            # cursor.execute("SELECT * FROM account_statement WHERE account_number = %s ORDER BY transaction_id DESC LIMIT 5", (account_number,))
            # last_five_transactions = cursor.fetchall()

            #Print the last five transactions
            # print("\nLast Five Transactions:")
            # for transaction in last_five_transactions:
            #     print(transaction)
            else:
               # API call failed
                print('API Error:', response.status_code, response.text) 
                return ""          

        def loan_statement():
            print("loan statemet call made")
            data = {
            "messages": [
            {
                "content": '''
                You are designed to answer queries received from bank users. Please classify the question asked into intent described below. Give answer in one word. I need intent only in one word, I am using your output to use a switch case: 
                classify the mail into below 4 categories. Do not provide any extra explanation.
                AccountStatement = balance statement for account
                loanDue = Regarding the loan amount.
                genQuery = if user is asking general questions related to banking, not specific about any user account or user specific services.
                Complaints = categorise user conplaints in this category
                category. 
                If more than one query is asked give answer in a list.
                Do not overthink or assume the intent behind the message other than what is directly described in the message. Do not justify yourself. I am using your output in my code, just give one word answer.
                Do not assume any other category. If the message strictly belongs to above categories, then only categorize that. If you are not sure. Please categorize as compla and do not provide any other explanation when message comes under  category.
                Do not assume fund transfer as loan payment, it can be any other type of fund transfer, just give output as "NotAvailable"  only, no other explanation.
                ''',
                "role": "system"
                },
                {
                "content": input_mail,
                "role": "user"
                }
            ]
            }
            # Make a POST request to the API endpoint with the data
            response = requests.post(API_URL, json=data)
            # Check the response from the API
            if response.status_code == 200:
            # API call successful
                api_response = response.json()
                print('API Response:', api_response)
        
                content = api_response['choices'][0]['message']['content']
                print('Content:', content)
            else:
            # API call failed
                print('API Error:', response.status_code, response.text)
        
        def credit_statement():
            print("credit statemet call made")
            data = {
            "messages": [
            {
            "content": '''
                You are designed to get data from emails received from user for a bank. 
                I want specific keywords from the message as described below. Just answer in the format described below, nothing else.

                if user wants to know the current outstanding balance on their loan. give information in the format below:
                            "Loan Balance Inquiry" = {}

                if user is inquiring about their past payments, including the dates and amounts paid. give information in the format below:
                            "Payment History" = {}

                if user wants to know the interest rate associated with their loan. give information in the format below:
                            "Interest Rate Inquiry" = {}

                if user is requesting a payoff quote to determine the total amount needed to pay off their loan in full. give information in the format below:
                            "Loan Payoff Quote" = {}

                If user is asking for anything else other than categories mentioned above, then just give which is given below.
                            "unavailable" = {}

                Do not justify or explain yourself. Answer in the prescribed format only.
                ''',
            "role": "system"
            },
            {
            "content": input_mail,
            "role": "user"
            }
        ]
        }
        # Make a POST request to the API endpoint with the data
            response = requests.post(API_URL, json=data)
        # Check the response from the API
            if response.status_code == 200:
                # API call successful
                api_response = response.json()
                print('API Response:', api_response)
                
                content = api_response['choices'][0]['message']['content']
                print('Content:', content)
            else:
            # API call failed
                print('API Error:', response.status_code, response.text)
        def switch_case(content):
            print("\ncategory:", content)
            switch = {
                'AccountStatement': account_statement,
                'LoanStatement': loan_statement,
                'CreditStatement': credit_statement
                }
            content = content.lower().strip()
    
            switch.get(content, "Invalid content")

            if 'accountstatement' in content:
                data, context = account_statement()
                email_res = email_generation(context)
            elif content == 'LoanStatement':
                loan_statement()
            elif content == 'CreditStatement':
                credit_statement()
            else:
                print("information not found")
        result = switch_case(content)
    else:
        # API call failed
        print('API Error:', response.status_code, response.text)
except mysql.connector.Error as error:
        print("Error:", error)
finally:
    # Close the cursor and connection
    if 'connection' in locals():
        cursor.close()
        connection.close()