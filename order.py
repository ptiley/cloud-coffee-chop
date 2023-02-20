import json
import boto3
import uuid

def lambda_handler(event, context):
    print(event)
    clientDrink = boto3.client("dynamodb")
    clientFood = boto3.client("dynamodb")
    clientOrder = boto3.client("dynamodb")
    
    body = event.get('body')
    bodyDict = json.loads(body)
    bodyList = bodyDict.get('order')

    index = 0
    orderedItems = []
    usersBill = 0

    while(index < len(bodyList)) :
        orderItem = bodyList[index]
        orderedItemKeyList = list(orderItem.keys())
        orderedItem = orderedItemKeyList[0]
        key ={'drinkName':{'S':orderedItem}}
        drinkResponse = clientDrink.get_item(TableName = "drinksMenu",Key = key)
        key ={'foodName':{'S':orderedItem}}
        foodResponse = clientFood.get_item(TableName = "foodMenu",Key = key)
        menuItem = drinkResponse.get('Item')
        if(menuItem is not None) :
            costItem = menuItem.get('price')
            cost = costItem.get('N')
            itemDrinkName = menuItem.get('drinkName')
            itemDrink = itemDrinkName.get('S')
            usersBill = usersBill + float(cost)
            orderedItems.append(itemDrink)
        else :
            menuItem = foodResponse.get('Item')
            costItem = menuItem.get('price')
            cost = costItem.get('N')
            usersBill = usersBill + float(cost)
            itemFoodName = menuItem.get('foodName')
            print("itemFoodName: "+str(itemFoodName)+" "+str(type(itemFoodName)))
            itemFood = itemFoodName.get('S')
            print("itemFood: "+str(itemFood)+" "+str(type(itemFood)))
            orderedItems.append(itemFood)
        
        index = index + 1
        print("index "+str(index))

    orderID = str(uuid.uuid4())
    print(orderID)
    item = {
        "orderID": {"S":orderID},
        "Bill": {"N":str(usersBill)},
        "Ordered": {"S": str(orderedItems)}
    }
    clientOrder.put_item(TableName = 'orders', Item = item)

    return {
        'statusCode': 200,
        'body': json.dumps("usersBill: "+str(usersBill))
    }
