import os
import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

# Configura o layout visual do FastF1 e Matplotlib sem avisos
fastf1.plotting.setup_mpl()

# Garante que a pasta 'cache' exista antes de ativar o cache
if not os.path.exists('cache'):
    os.makedirs('cache')

fastf1.Cache.enable_cache('cache')

print("Baixando dados do GP de São Paulo (Interlagos) - 2023...")

# Carrega a sessão de Corrida (R = Race)
session = fastf1.get_session(2023, 'São Paulo', 'R')
session.load()

# Pega a volta mais rápida da corrida inteira
fastest_lap = session.laps.pick_fastest()
driver_code = fastest_lap['Driver']
lap_time = fastest_lap['LapTime']

print(f"\nVolta mais rápida: {driver_code} com o tempo de {lap_time}")
print("Processando telemetria da volta...")

# Extrai os dados de telemetria da volta (Velocidade, Posição X/Y no circuito)
telemetry = fastest_lap.get_telemetry()

# Prepara os dados de coordenadas (X, Y) e velocidade
x = telemetry['X'].values
y = telemetry['Y'].values
speed = telemetry['Speed'].values

# Prepara os segmentos de linha para colorir o circuito com base na velocidade
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Cria a figura e o gráfico
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor('#1e1e1e')
ax.set_facecolor('#1e1e1e')

# Define a paleta de cores (Plasma: roxo = devagar, amarelo = alta velocidade)
norm = plt.Normalize(speed.min(), speed.max())
lc = LineCollection(segments, cmap='plasma', norm=norm, linewidth=5)
lc.set_array(speed)
line = ax.add_collection(lc)

# Adiciona a barra de legenda da velocidade no lado
cb = fig.colorbar(line, ax=ax, orientation='vertical', pad=0.02)
cb.set_label('Velocidade (km/h)', color='white', fontsize=12)
cb.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cb.ax, 'yticklabels'), color='white')

# Estiliza os títulos
ax.set_title(f"Telemetria de Velocidade - Interlagos 2023\nVolta Mais Rápida: {driver_code} ({lap_time})", 
             color='white', fontsize=14, fontweight='bold', pad=15)

# Remove os eixos numéricos para focar apenas no mapa do circuito
ax.axis('off')
ax.autoscale()

# Salva a imagem gerada para usar depois no README do GitHub
plt.savefig('interlagos_telemetria.png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())

print("\nSucesso! Imagem 'interlagos_telemetria.png' salva na pasta do projeto.")
print("Exibindo o gráfico na tela...")
plt.show()