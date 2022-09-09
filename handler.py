import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def setUser(event, context):
    primaryKeyId=0
    # TODO implement
    
    #LEGGO LA TABELLA DAL DYNAMODB
    dynamodb=boto3.resource('dynamodb')
    table = dynamodb.Table('tabellaUtente') 
    
    #EVENTO : PASSAGGIO PARAMETRI ID E NOME
    idUser=event['idUser']
    nome=event['nomeUser']
    
    #LEGGO TUTTI GLI ID DELLA TABELLA
    table2 = dynamodb.Table('id') 
    
    #MESSAGGIO PER LA CREAZIONE DELL'USER CORRETTA
    creatoReply = {
        "message": "creato user!",
        "input": event,
    }
    
    #MESSAGGIO PER LA CREAZIONE DELL'USER NON CORRETTA
    nonCreatoReply = {
        "message": "id in uso, non ho creato l'utente!",
        "input": event,
    }
    
    #CONTO SE C'è UN ID CON LO STESSO NUMERO
    response = table.query(
        KeyConditionExpression=Key('id').eq(idUser)
        )
    
    #PER OGNI ID TROVATO INCREMENTA DI +1 IL CONTATORE
    for i in response['Items']:
        primaryKeyId=primaryKeyId+1
        i=response['Items']    #esco dal ciclo perchè me ne basta uno 
    
    #SE IL CONTATORE =0
    if(primaryKeyId==0):
        table.put_item(Item={#scrivi le credenziali nella tabella
            'id': idUser,
            'nome': nome,
        })
        response = {"statusCode": 200, "body": json.dumps(creatoReply)}
        
    #SE CONTATORE>0
    if(primaryKeyId>0):
        response = {"statusCode": 200, "body": json.dumps(nonCreatoReply)}#messaggio di errore
        return response

    return response
        

def getIdUser(event, context):
    primaryKeyId=0
    
    #LEGGO LA TABELLA DAL DYNAMODB
    dynamodb=boto3.resource('dynamodb')
    table = dynamodb.Table('tabellaUtente') 
    
    #EVENTO : PASSAGGIO PARAMETRI ID E NOME
    idUser=event['idUser']
    
    #LEGGO TUTTI GLI ID DELLA TABELLA
    table2 = dynamodb.Table('id') 
    
    
    #MESSAGGIO PER IL RILEVAMENTO DELL'ID 
    trovatoReply = {
        "message": "id trovato all'interno della tabella",
        "input": event,
    }
    
    #MESSAGGIO ERRORE
    nonTrovatoReply = {
        "message": "id NON trovato all'interno della tabella",
        "input": event,
    }
    
    #CONTO GLI ID CON LO STESSO NUMERO
    response = table.query(
        KeyConditionExpression=Key('id').eq(idUser)
        )
    for i in response['Items']:
        primaryKeyId=primaryKeyId+1
    
    #SE ESISTE UN'ALTRO ID CON LO STESSO VALORE 
    if(primaryKeyId>0):
        #response = {"statusCode": 200, "body": json.dumps(trovatoReply)}
        response= (i['id'], ":",i['nome']) #scrivi l'user
        return response
    #SE L'ID CERCATO NON ESISTE
    if(primaryKeyId==0):
        response = {"statusCode": 200, "body": json.dumps(nonTrovatoReply)} #scrivi messaggio errore
    
    return response
