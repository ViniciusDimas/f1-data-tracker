import os
import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
import numpy as np

fastf1.plotting.setup_mpl()

if not os.path.exists('cache'):
    os.makedirs('cache')

fastf1.Cache.enable_cache('cache')

def pegar_cor_piloto(piloto_code, session):
    try:
        return fastf1.plotting.get_driver_color(piloto_code, session=session)
    except AttributeError:
        try:
            return fastf1.plotting.driver_color(piloto_code)
        except Exception:
            return '#FFFFFF'

def comparar_pilotos():
    print("\n" + "="*50)
    print("      COMPARADOR DE TELEMETRIA ENTRE PILOTOS      ")
    print("="*50)
    
    ano_str = input("\nDigite o ano da temporada (ex: 2021, 2023, 2024): ").strip()
    if not ano_str.isdigit():
        print("Ano inválido!")
        return
    ano = int(ano_str)
    
    gp = input("Digite o nome ou país do GP (ex: São Paulo, Monza, Abu Dhabi): ").strip()
    
    piloto1_code = input("Digite a sigla do Piloto 1 (ex: VER, LEC): ").strip().upper()
    piloto2_code = input("Digite a sigla do Piloto 2 (ex: HAM, SAI): ").strip().upper()

    print(f"\n[1/4] Carregando dados do GP de {gp} ({ano})...")
    
    try:
        session = fastf1.get_session(ano, gp, 'R')
        session.load()

        try:
            lap1 = session.laps.pick_drivers(piloto1_code).pick_fastest()
            lap2 = session.laps.pick_drivers(piloto2_code).pick_fastest()
        except AttributeError:
            lap1 = session.laps.pick_driver(piloto1_code).pick_fastest()
            lap2 = session.laps.pick_driver(piloto2_code).pick_fastest()

        cor_p1 = pegar_cor_piloto(piloto1_code, session)
        cor_p2 = pegar_cor_piloto(piloto2_code, session)

        print(f"[2/4] Processando voltas: {piloto1_code} ({lap1['LapTime']}) vs {piloto2_code} ({lap2['LapTime']})...")

        tel1 = lap1.get_telemetry().add_distance()
        tel2 = lap2.get_telemetry().add_distance()

        distancia_comum = np.linspace(0, max(tel1['Distance'].max(), tel2['Distance'].max()), 1000)
        
        speed1 = np.interp(distancia_comum, tel1['Distance'], tel1['Speed'])
        speed2 = np.interp(distancia_comum, tel2['Distance'], tel2['Speed'])
        
        x = np.interp(distancia_comum, tel1['Distance'], tel1['X'])
        y = np.interp(distancia_comum, tel1['Distance'], tel1['Y'])

        print("[3/4] Identificando quem foi mais rápido em cada trecho...")

        delta_v = speed1 > speed2

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        print("[4/4] Gerando mapa de comparação de forças...")
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor('#1e1e1e')
        ax.set_facecolor('#1e1e1e')

        cmap = ListedColormap([cor_p2, cor_p1])

        lc = LineCollection(segments, cmap=cmap, linewidth=5)
        lc.set_array(delta_v[:-1]) 
        ax.add_collection(lc)

        ax.set_title(f"Domínio de Velocidade: {gp} {ano}\n{piloto1_code} vs {piloto2_code}", 
                     color='white', fontsize=14, fontweight='bold', pad=15)

        legend_elements = [
            Line2D([0], [0], color=cor_p1, lw=4, label=f'{piloto1_code} mais rápido ({lap1["LapTime"]})'),
            Line2D([0], [0], color=cor_p2, lw=4, label=f'{piloto2_code} mais rápido ({lap2["LapTime"]})')
        ]
        ax.legend(handles=legend_elements, loc='upper right', facecolor='#2b2b2b', edgecolor='none', labelcolor='white')

        ax.axis('off')
        ax.autoscale()

        nome_arquivo = f"comparacao_{piloto1_code}_vs_{piloto2_code}_{gp.lower()}_{ano}.png".replace(" ", "_")
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())

        print(f"\n🎉 Sucesso! Gráfico salvo como '{nome_arquivo}'.")
        print("Exibindo janela do gráfico...")
        plt.show()

    except Exception as e:
        print(f"\n[ERRO] Não foi possível comparar os pilotos. Verifique as siglas e se ambos correram essa prova.\nDetalhes: {e}")

if __name__ == "__main__":
    comparar_pilotos()