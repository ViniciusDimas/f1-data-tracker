#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PILOTOS 20
#define TAM_NOME 50

typedef struct {
    char nome[TAM_NOME];
    int titulos;
    int vitorias;
    int podios;
    int poles;
    int corridas;
} Piloto;

// Função portátil para limpar a tela
void limparTela() {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}

int carregarDados(const char *nomeArquivo, Piloto pilotos[]) {
    FILE *file = fopen(nomeArquivo, "r");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo %s!\n", nomeArquivo);
        return 0;
    }

    char linha[256];
    int count = 0;

    fgets(linha, sizeof(linha), file); // Ignora cabeçalho

    while (fgets(linha, sizeof(linha), file) && count < MAX_PILOTOS) {
        char *token = strtok(linha, ",");
        strcpy(pilotos[count].nome, token);

        token = strtok(NULL, ",");
        pilotos[count].titulos = atoi(token);

        token = strtok(NULL, ",");
        pilotos[count].vitorias = atoi(token);

        token = strtok(NULL, ",");
        pilotos[count].podios = atoi(token);

        token = strtok(NULL, ",");
        pilotos[count].poles = atoi(token);

        token = strtok(NULL, ",\n");
        pilotos[count].corridas = atoi(token);

        count++;
    }

    fclose(file);
    return count;
}

void exibirPiloto(Piloto p, int pos) {
    float aproveitamentoPodio = ((float)p.podios / p.corridas) * 100.0;
    float aproveitamentoVitoria = ((float)p.vitorias / p.corridas) * 100.0;

    if (pos > 0) {
        printf(" %d LUGAR: %s\n", pos, p.nome);
    } else {
        printf(" Piloto: %s\n", p.nome);
    }
    printf("----------------------------------------\n");
    printf(" Titulos Mundiais: %d\n", p.titulos);
    printf(" Vitorias:        %d (%.1f%% de aproveitamento)\n", p.vitorias, aproveitamentoVitoria);
    printf(" Podios:          %d (%.1f%% de aproveitamento)\n", p.podios, aproveitamentoPodio);
    printf(" Pole Positions:  %d\n", p.poles);
    printf(" Corridas:        %d\n", p.corridas);
    printf("========================================\n\n");
}

void ordenarPilotos(Piloto pilotos[], int total, int criterio) {
    Piloto temp;
    for (int i = 0; i < total - 1; i++) {
        for (int j = 0; j < total - i - 1; j++) {
            int precisaTrocar = 0;

            if (criterio == 1) { // Vitórias
                if (pilotos[j].vitorias < pilotos[j + 1].vitorias) precisaTrocar = 1;
            } 
            else if (criterio == 2) { // Pódios
                if (pilotos[j].podios < pilotos[j + 1].podios) precisaTrocar = 1;
            } 
            else if (criterio == 3) { // Títulos
                if (pilotos[j].titulos < pilotos[j + 1].titulos) precisaTrocar = 1;
            } 
            else if (criterio == 4) { // % Pódios
                float ap1 = ((float)pilotos[j].podios / pilotos[j].corridas) * 100.0;
                float ap2 = ((float)pilotos[j + 1].podios / pilotos[j + 1].corridas) * 100.0;
                if (ap1 < ap2) precisaTrocar = 1;
            }

            if (precisaTrocar) {
                temp = pilotos[j];
                pilotos[j] = pilotos[j + 1];
                pilotos[j + 1] = temp;
            }
        }
    }
}

int main() {
    Piloto pilotos[MAX_PILOTOS];
    int totalPilotos = carregarDados("brasileiros_f1.csv", pilotos);

    if (totalPilotos == 0) {
        printf("Certifique-se de que o arquivo 'brasileiros_f1.csv' esta na mesma pasta.\n");
        return 1;
    }

    int opcao;
    do {
        limparTela();
        printf("=== BANCO DE DADOS: BRASILEIROS NA F1 ===\n");
        printf("1. Listar todos os pilotos (ordem original)\n");
        printf("2. Buscar piloto por nome\n");
        printf("3. Ver Ranking de Pilotos (Ordenar)\n");
        printf("0. Sair\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        getchar();

        if (opcao == 1) {
            limparTela();
            printf("--- LISTA COMPLETA ---\n\n");
            for (int i = 0; i < totalPilotos; i++) {
                exibirPiloto(pilotos[i], 0);
            }
            printf("Pressione ENTER para voltar...");
            getchar();
        } 
        else if (opcao == 2) {
            limparTela();
            char busca[TAM_NOME];
            printf("Digite o nome do piloto: ");
            fgets(busca, TAM_NOME, stdin);
            busca[strcspn(busca, "\n")] = 0;

            limparTela();
            int encontrado = 0;
            for (int i = 0; i < totalPilotos; i++) {
                if (strstr(pilotos[i].nome, busca) != NULL) {
                    exibirPiloto(pilotos[i], 0);
                    encontrado = 1;
                }
            }
            if (!encontrado) printf("Piloto nao encontrado.\n");
            
            printf("Pressione ENTER para voltar...");
            getchar();
        }
        else if (opcao == 3) {
            limparTela();
            int criterio;
            printf("--- GERAR RANKING DE PILOTOS ---\n");
            printf("1. Maior quantidade de Vitorias\n");
            printf("2. Maior quantidade de Podios\n");
            printf("3. Maior quantidade de Titulos\n");
            printf("4. Maior Eficiencia (%% de Podios/Corrida)\n");
            printf("Escolha o criterio: ");
            scanf("%d", &criterio);
            getchar();

            if (criterio >= 1 && criterio <= 4) {
                ordenarPilotos(pilotos, totalPilotos, criterio);
                limparTela();
                printf("--- RANKING RESULTANTE ---\n\n");
                for (int i = 0; i < totalPilotos; i++) {
                    exibirPiloto(pilotos[i], i + 1); // Passa a posição (1º, 2º, etc.)
                }
            } else {
                printf("\nOpcao invalida!\n");
            }
            printf("Pressione ENTER para voltar...");
            getchar();
        }

    } while (opcao != 0);

    limparTela();
    printf("Programa encerrado!\n");
    return 0;
}