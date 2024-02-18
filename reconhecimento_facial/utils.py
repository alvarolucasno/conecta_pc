import boto3
from django.conf import settings


def adicionar_face(imagem_bytes):
    client = boto3.client('rekognition')

    response = client.detect_faces(Image={'Bytes': imagem_bytes}, Attributes=['DEFAULT'])

    num_faces = len(response['FaceDetails'])

    if num_faces == 0:
        raise ValueError("Nenhuma face detectada na imagem.")
    elif num_faces > 1:
        raise ValueError("A fotografia enviada possui mais de uma face. Favor reenviar outra.")

    response = client.index_faces(CollectionId=settings.AWS_COLLECTION_ID,
                                  Image={'Bytes': imagem_bytes},
                                  DetectionAttributes=['DEFAULT'])

    if response['FaceRecords']:
        face_id = response['FaceRecords'][0]['Face']['FaceId']
        return True, face_id
    else:
        raise Exception("Não foi possível adicionar a face à coleção.")

def reconhecer_face(imagem_bytes):
    client = boto3.client('rekognition')

    response = client.search_faces_by_image(CollectionId=settings.AWS_COLLECTION_ID,
                                            Image={'Bytes': imagem_bytes},
                                            FaceMatchThreshold=80)

    face_matches = response['FaceMatches']

    if not face_matches:
        return (False, "Nenhuma correspondência encontrada.")

    sorted_matches = sorted(face_matches, key=lambda x: x['Similarity'], reverse=True)
    resultados = [{'FaceId': match['Face']['FaceId'], 'similaridade': match['Similarity']} for match in sorted_matches]

    return (True, resultados)

def remover_face(face_id_aws):

    client = boto3.client('rekognition')

    try:
        response = client.delete_faces(
            CollectionId=settings.AWS_COLLECTION_ID,
            FaceIds=[face_id_aws]
        )
        return True
    except Exception as e:
        raise ValueError(f"Erro ao remover face: {e}")