from datetime import datetime, timedelta
from django.db.models import Count
from gym.models.workout_record import WorkoutRecord

def calcular_streak_usuario(user, group, Obj):
    membership = Obj.objects.get(user=user, group=group)
    meta_semanal = membership.meta_semanal
    data_entrada = membership.data_entrada
    
    semanas = gerar_semanas_desde_entrada(data_entrada)
    
    streak_atual = 0
    melhor_streak = membership.melhor_streak
    falhas_consecutivas = 0
    
    for semana in semanas:
        treinos_na_semana = contar_treinos_semana(user, group, semana)
        status_semana = classificar_semana(treinos_na_semana, meta_semanal)
        
        if status_semana in ['SUCESSO', 'TOLERANCIA']:
            streak_atual += 1
            falhas_consecutivas = 0
        else:  
            falhas_consecutivas += 1
            
            if falhas_consecutivas >= 2:
                melhor_streak = max(melhor_streak, streak_atual)
                streak_atual = 0
                falhas_consecutivas = 0
    
    membership.streak_atual = streak_atual
    membership.melhor_streak = max(melhor_streak, streak_atual)
    membership.save()
    
    return streak_atual

def classificar_semana(treinos_realizados, meta_semanal):
    if treinos_realizados >= meta_semanal:
        return 'SUCESSO'
    elif treinos_realizados >= max(1, meta_semanal - 1):  # Tolerância
        return 'TOLERANCIA'
    else:
        return 'FALHA'

def gerar_semanas_desde_entrada(data_entrada):
    semanas = []
    hoje = datetime.now().date()
    
    inicio_semana = data_entrada - timedelta(days=data_entrada.weekday())
    
    while inicio_semana <= hoje:
        fim_semana = min(inicio_semana + timedelta(days=6), hoje)
        semanas.append((inicio_semana, fim_semana))
        inicio_semana += timedelta(days=7)
    
    return semanas

def contar_treinos_semana(user, group, semana):
    inicio, fim = semana
    return WorkoutRecord.objects.filter(
        user=user,
        group=group,
        data_treino__range=(inicio, fim)
    ).count()

def get_status_semana_atual(user, group,  Obj):
    hoje = datetime.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    
    treinos_esta_semana = contar_treinos_semana(user, group, (inicio_semana, fim_semana))
    membership = Obj.objects.get(user=user, group=group)
    
    return {
        'treinos_realizados': treinos_esta_semana,
        'meta_semanal': membership.meta_semanal,
        'status': classificar_semana(treinos_esta_semana, membership.meta_semanal),
        'dias_restantes': (fim_semana - hoje).days + 1
    }