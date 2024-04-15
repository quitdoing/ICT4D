from flask import Flask, request, Response
import pandas as pd

app = Flask(__name__)

# Load the Excel file into a Pandas DataFrame
data = pd.read_excel('data.xlsx')

@app.route('/submit', methods=['POST'])
def submit():
    # Get the phone number from request
    phone = request.args.get('caller_number')
    print(phone)

    # Query the certifiate number from the Excel file
    result = data.loc[data['Phone'] == int(phone), 'Number'].tolist()

    print(result)
    print(type(result))

    # Check if the result list is empty
    if not result:
        result = 'Your certificate is not issued yet.'
    else:
        result = 'Your certificate number is ' + ' and '.join(str(x) for x in result)

    # Construct the xml response
    xml_response = '''<?xml version="1.0" encoding="UTF-8"?>
    <vxml xmlns="http://www.w3.org/2001/vxml"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.w3.org/2001/vxml
    http://www.w3.org/TR/voicexml20/vxml.xsd"
    version="2.0">
     <form>
        <block>{}</block>
     </form>
    </vxml>'''.format(result)

    # 返回XML响应
    return Response(xml_response, mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
