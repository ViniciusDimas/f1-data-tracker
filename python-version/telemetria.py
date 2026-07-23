import os
import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

fastf1.plotting.setup_mpl()

if not os.path.exists('cache'):
    os.makedirs('cache')

fastf1.Cache.enable_cache('cache')

def gerar_grafico_telemetria():
    print("\n" + "="*50)
    print("      ANALISADOR DE TELEMETRIA DA FÓRMULA 1      ")
    print("="*50)
    
    ano_str = input("\nDigite o ano da temporada (ex: 2021, 2022, 2023, 2024): ").strip()
    if not ano_str.isdigit():
        print("Ano inválido!")
        return
    ano = int(ano_str)
    
    gp = input("Digite o nome ou país do GP (ex: São Paulo, Bahrain, Monza, Monaco): ").strip()
    if not gp:
        print("GP inválido!")
        return
        
    piloto = input("Digite a sigla do piloto (ex: VER, HAM, SEN, LEC, NOR) ou aperte Enter para a 'Volta Mais Rápida': ").strip().upper()

    print(f"\n[1/3] Baixando dados do GP de {gp} ({ano})...")
    
    try:
        session = fastf1.get_session(ano, gp, 'R')
        session.load()
        
        if piloto:
            laps = session.laps.pick_driver(piloto)
            if laps.empty:
                print(f"Nenhum dado encontrado para o piloto {piloto} nesta corrida.")
                return
            lap = laps.pick_fastest()
        else:
            lap = session.laps.pick_fastest()

        driver_code = lap['Driver']
        lap_time = lap['LapTime']
        
        print(f"[2/3] Processando a melhor volta de {driver_code} ({lap_time})...")

        telemetry = lap.get_telemetry()
        
        x = telemetry['X'].values
        y = telemetry['Y'].values
        speed = telemetry['Speed'].values

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        print("[3/3] Desenhando mapa de velocidade...")
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor('#1e1e1e')
        ax.set_facecolor('#1e1e1e')

        norm = plt.Normalize(speed.min(), speed.max())
        lc = LineCollection(segments, cmap='plasma', norm=norm, linewidth=5)
        lc.set_array(speed)
        line = ax.add_collection(lc)

        cb = fig.colorbar(line, ax=ax, orientation='vertical', pad=0.02)
        cb.set_label('Velocidade (km/h)', color='white', fontsize=12)
        cb.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cb.ax, 'yticklabels'), color='white')

        ax.set_title(f"Telemetria de Velocidade: {gp} {ano}\nPiloto: {driver_code} | Tempo: {lap_time}", 
                     color='white', fontsize=14, fontweight='bold', pad=15)

        ax.axis('off')
        ax.autoscale()

        nome_arquivo = f"{gp.lower()}_{driver_code}_{ano}_telemetria.png".replace(" ", "_")
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())

        print(f"\n🎉 Sucesso! Gráfico salvo como '{nome_arquivo}'.")
        print("Exibindo janela do gráfico...")
        plt.show()

    except Exception as e:
        print(f"\n[ERRO] Não foi possível carregar os dados. Verifique o nome do GP e o ano.\nDetalhes: {e}")

if __name__ == "__main__":
    gerar_grafico_telemetria()