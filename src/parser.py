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

falhas_por_ip = (
    logs[logs["event"] == "login_failed"]["source_ip"]
    .value_counts()
)

print ("\nFalhas de login por ip:")
print (falhas_por_ip)

limites = 3

ips_suspeitos = falhas_por_ip[falhas_por_ip >= limites]

print(f"\nIPs suspeitos - Total {limites} falhas:")
print(ips_suspeitos)