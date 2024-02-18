from django.http import JsonResponse
from django.shortcuts import render
from reconhecimento_facial.utils import reconhecer_face
from presos.models import Preso
from mandados.models import Procurados

def reconhecimento_facial(request):
    if request.method == 'POST' and request.FILES:
        foto = request.FILES['foto']
        imagem_bytes = foto.read()

        reconhecido, resultados = reconhecer_face(imagem_bytes)

        if reconhecido:
            presos_encontrados = []
            procurados_encontrados = []

            for resultado in resultados:
                face_id = resultado['FaceId']
                
                presos = Preso.objects.filter(face_id_aws=face_id)
                procurados = Procurados.objects.filter(face_id_aws=face_id)
                
                for preso in presos:
                    presos_encontrados.append({
                        'frontal': preso.frontal.url if preso.frontal else None,  # Ajuste para o campo correto
                        'nome_completo': preso.nome_completo,
                        'data_nascimento': preso.data_nascimento.strftime('%d/%m/%Y') if preso.data_nascimento else None,
                        'mae': preso.mae,
                        'pai': preso.pai,
                        'cpf': preso.cpf,
                    })

                for procurado in procurados:
                    procurados_encontrados.append({
                        'foto': procurado.foto.url if procurado.foto else None,  # Ajuste para o campo correto
                        'nome_completo': procurado.nome_completo,
                        'data_nascimento': procurado.data_nascimento.strftime('%d/%m/%Y') if procurado.data_nascimento else None,
                        'mae': procurado.mae,
                        'pai': procurado.pai,
                        'cpf': procurado.cpf,
                    })

            dados_resposta = {
                'sucesso': True,
                'presos': presos_encontrados,
                'procurados': procurados_encontrados,
            }

            return JsonResponse(dados_resposta)
        else:
            return JsonResponse({'sucesso': False, 'mensagem': resultados})

    return render(request, 'reconhecimento_facial/consulta.html')