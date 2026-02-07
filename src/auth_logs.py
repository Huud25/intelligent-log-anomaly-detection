from __future__ import annotations  #Mantém as funcionalidades para strings futuras.

from dataclasses import dataclass   #Organiza dados no código.
from pathlib import Path            #Acessa os arquivos com segurança.

import pandas as pd     #Importa a biblioteca "pandas" e transforma o módulo em "pd".

REQUIRED_COLUMNS = [    #Colunas obrigatórias.
    "timestamp",        #Data/Hora.
    "username",         #Nome de usuário
    "source_ip",        #Ip de origem.
    "event",            #Evento (tipo de ação realizada).
    "country",          #País (localização geográfica do ip de origem).
    "user_agent",       #Agente do usuário (navegador/sistema operacional).
]

ALLOWED_EVENTS = {"login_success", "login_failed"}  #Eventos permitidos.

@dataclass(frozen=True)             #Essa classe é imutável.

class AuthLogs:              #Registros de autenticação.
    """Container para logs já validados e prontos para análise"""
    df: pd.DataFrame        

def load_auth_logs(csv_path: str | Path) -> AuthLogs:
    """
    Carrega logs de autenticação a partir de um CSV e valida:
    - colunas obrigatórias
    - timestamp parseável
    - valores de eventos permitidos
    - normalização básica de strings
    """

    path = Path(csv_path)

    if not path.exists():   #Verifica se o arquivo existe.
     raise FileNotFoundError (f"Arquivo não encontrado: {path}")

    df = pd.read_csv(path)  #Grade de linhas e colunas.

    _validate_columns(df)       #Validar/checar se o formato esta correto.
    _normalize_strings(df)      #Padronizar os textos.
    _parse_timestamps(df)      #Interpretar/converter datas/horas.
    _validate_event_values(df)  #Garantir que os eventos são válidos.
 
    df = df[REQUIRED_COLUMNS].copy()   #Mantém apenas colunas conhecidas.

    df = df.sort_values("timestamp", kind = "stable").reset_index(drop=True)  # Ordenar por tempo, ajuda detectores e evita resultados inconsistentes.

    return AuthLogs(df=df)     #Passe o valor da variável df para o parâmetro df do AuthLogs.

def _validate_columns(df: pd.DataFrame) -> None: 
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Faltam colunas obrigatórias: {missing}")

def _normalize_strings(df: pd.DataFrame) -> None:
    for col in ["username", "source_ip", "event", "country", "user_agent"]:
        df[col] = df[col].astype(str).str.strip()

def _parse_timestamps(df: pd.DataFrame) -> None:
    df["timestamp"] = pd.to_datatime(df["timestamp"], errors="coerce")
    if df["timestamp"].isna().any():
        n = int(df["timestamp"].isna().sum())
        raise ValueError(f"{n} timestamp(s) inválido(s). Use ISO, ex: 2026-02-06T08:40:07-03:00")
    
def _validate_event_values(df: pd.DataFrame) -> None:
    invalid = df.loc[~df["event"].isin(ALLOWED_EVENTS), "event"].unique().tolist()
    if invalid:
        raise ValueError(f"Valores inválidos em 'event': {invalid}. Permitidos: {sorted(ALLOWED_EVENTS)}")






