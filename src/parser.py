import pandas as pd

logs = pd.read_csv("data/raw/auth_logs.csv")

print ("Total de linhas:", len(logs))

contagem = logs["event"].value_counts()
print ("\nContagem por tipo de evento:")
print (contagem)

falhas_por_usuario = (
    logs[logs["event"] == "login_failed"]["username"]
    .value_counts()
)

print ("\nFalhas de login por usuário:")
print (falhas_por_usuario)
