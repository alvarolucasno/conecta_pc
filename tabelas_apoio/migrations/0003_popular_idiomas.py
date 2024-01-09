from django.db import migrations

def popular_idiomas(apps, schema_editor):
    Idioma = apps.get_model('tabelas_apoio', 'Idioma')

    idiomas = [
        {"nome": "Mandarim", "codigo_iso": "zh"},
        {"nome": "Espanhol", "codigo_iso": "es"},
        {"nome": "Inglês", "codigo_iso": "en"},
        {"nome": "Hindi", "codigo_iso": "hi"},
        {"nome": "Bengali", "codigo_iso": "bn"},
        {"nome": "Russo", "codigo_iso": "ru"},
        {"nome": "Japonês", "codigo_iso": "ja"},
        {"nome": "Punjabi", "codigo_iso": "pa"},
        {"nome": "Marathi", "codigo_iso": "mr"},
        {"nome": "Telugu", "codigo_iso": "te"},
        {"nome": "Wu (Shanghainese)", "codigo_iso": "wuu"},
        {"nome": "Turco", "codigo_iso": "tr"},
        {"nome": "Coreano", "codigo_iso": "ko"},
        {"nome": "Francês", "codigo_iso": "fr"},
        {"nome": "Alemão", "codigo_iso": "de"},
        {"nome": "Vietnamita", "codigo_iso": "vi"},
        {"nome": "Tamil", "codigo_iso": "ta"},
        {"nome": "Urdu", "codigo_iso": "ur"},
        {"nome": "Javanês", "codigo_iso": "jv"},
        {"nome": "Italiano", "codigo_iso": "it"},
        {"nome": "Egípcio Árabe", "codigo_iso": "arz"},
        {"nome": "Gujarati", "codigo_iso": "gu"},
        {"nome": "Iraniano Persa", "codigo_iso": "fa"},
        {"nome": "Bhojpuri", "codigo_iso": "bho"},
        {"nome": "Min Nan", "codigo_iso": "nan"},
        {"nome": "Hakka", "codigo_iso": "hak"},
        {"nome": "Jin", "codigo_iso": "cjy"},
        {"nome": "Hausa", "codigo_iso": "ha"},
        {"nome": "Kannada", "codigo_iso": "kn"},
        {"nome": "Indonésio", "codigo_iso": "id"},
        {"nome": "Polaquês", "codigo_iso": "pl"},
        {"nome": "Yoruba", "codigo_iso": "yo"},
        {"nome": "Xhosa", "codigo_iso": "xh"},
        {"nome": "Maithili", "codigo_iso": "mai"},
        {"nome": "Birmanês", "codigo_iso": "my"},
        {"nome": "Oriya", "codigo_iso": "or"},
        {"nome": "Sundanês", "codigo_iso": "su"},
        {"nome": "Romeno", "codigo_iso": "ro"},
        {"nome": "Amárico", "codigo_iso": "am"},
        {"nome": "Fula", "codigo_iso": "ff"},
        {"nome": "Oromo", "codigo_iso": "om"},
        {"nome": "Igbo", "codigo_iso": "ig"},
        {"nome": "Ucraniano", "codigo_iso": "uk"},
        {"nome": "Sindhi", "codigo_iso": "sd"},
        {"nome": "Norte Africano Árabe", "codigo_iso": "ary"},
        {"nome": "Sinhala", "codigo_iso": "si"},
        {"nome": "Chittagonian", "codigo_iso": "ctg"},
        {"nome": "Curdo", "codigo_iso": "ku"},
        {"nome": "Seraiki", "codigo_iso": "skr"},
        {"nome": "Neerlandês", "codigo_iso": "nl"},
        {"nome": "Malaio", "codigo_iso": "ms"},
        {"nome": "Cebuano", "codigo_iso": "ceb"}
    ]

    for idioma in idiomas:
        Idioma.objects.create(nome=idioma['nome'], codigo_iso=idioma['codigo_iso'])

class Migration(migrations.Migration):

    dependencies = [
        ('tabelas_apoio', '0002_idioma'),
    ]

    operations = [
        migrations.RunPython(popular_idiomas),
    ]
