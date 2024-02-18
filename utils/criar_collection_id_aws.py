import boto3

def criar_collection(collection_id):
    
    # Criar um cliente Rekognition
    client = boto3.client('rekognition')
    response = client.create_collection(CollectionId=collection_id)
    print(response)

# Usar a função
criar_collection('conecta_pc')
