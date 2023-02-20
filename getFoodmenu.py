import json
import boto3

def lambda_handler(event, context):
    print(event)    
    
    menuList = []

    client = boto3.client("dynamodb")
    response = client.scan(TableName="foodMenu")
    
    print(response)

    menuDict = response.get('Items')
    index = 0
    while(index < len(menuDict)):
        foodMenuDictItem = menuDict[index].get('foodName')
        print(foodMenuDictItem)
        menuItem = foodMenuDictItem.get('S')
        
        priceMenuDictItem = menuDict[index].get('price')
        print(priceMenuDictItem)
        menuPrice = priceMenuDictItem.get('N')
        
        qtyMenuDictItem = menuDict[index].get('qty')
        print(qtyMenuDictItem)
        menuQty = qtyMenuDictItem.get('N')
        
        menuList.append(
            {menuItem:[{"price":menuPrice},{"qty":menuQty}]})
        index = index + 1
    
    return {
        'statusCode': 200,
        'body': json.dumps({"FoodMenu": menuList})
    }
    
