# core/precificacao_opcoes_monte_carlo.py
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def option_price_use_case(S0, K, T, r, sigma, num_simulacoes):
    """
    Simula o preço de opções de compra europeias usando o método de Monte Carlo.

    Args:
        S0 (float): Preço atual do ativo subjacente.
        K (float): Preço de exercício (strike) da opção.
        T (float): Tempo até o vencimento em anos.
        r (float): Taxa de juros livre de risco anual.
        sigma (float): Volatilidade anual do ativo subjacente.
        num_simulacoes (int): Número de simulações de Monte Carlo.

    Returns:
        tuple: (preco_opcao, ST_array, statistics)
            preco_opcao (float): Preço estimado da opção de compra europeia.
            ST_array (numpy.ndarray): Array dos preços simulados do ativo no vencimento.
            statistics (dict): Dicionário com estatísticas descritivas dos preços no vencimento.
    """
    # Gerar números aleatórios da distribuição normal padrão
    z = np.random.standard_normal(num_simulacoes)

    # Simular os preços do ativo subjacente no vencimento (ST)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)

    # Calcular o payoff da opção de compra europeia
    payoffs = np.maximum(ST - K, 0)

    # Calcular o preço da opção como a média dos payoffs descontados
    preco_opcao = np.exp(-r * T) * np.mean(payoffs)

    # Calcular estatísticas descritivas dos preços finais simulados
    statistics = {
        'Média': np.mean(ST),
        'Mediana': np.median(ST),
        'Desvio Padrão': np.std(ST),
        'Mínimo': np.min(ST),
        'Máximo': np.max(ST),
        'Preço da Opção (Descontado)': preco_opcao # Incluindo o preço da opção aqui
    }

    return preco_opcao, ST, statistics

def create_plots(ST_array, num_periods_placeholder=None):
    """
    Cria gráficos para visualização dos resultados da simulação.
    Para a precificação de opções, podemos mostrar a distribuição dos preços finais.
    O 'price_plot' será mais conceitual ou omitido, pois não simulamos caminhos ao longo do tempo aqui.
    """
    # Gráfico de Distribuição dos Preços Finais
    plt.figure(figsize=(8, 6))
    plt.hist(ST_array, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('Distribuição dos Preços do Ativo no Vencimento (ST)')
    plt.xlabel('Preço do Ativo no Vencimento')
    plt.ylabel('Densidade')
    plt.grid(True)
    buf_dist = io.BytesIO()
    plt.savefig(buf_dist, format='png')
    plt.close()
    data_dist = base64.b64encode(buf_dist.getvalue()).decode('utf-8')

    # Para o "price_plot", como não temos caminhos ao longo do tempo,
    # podemos criar um gráfico de payoff ou apenas um placeholder.
    # Por simplicidade, vamos criar um gráfico de barras simples do payoff médio vs. zero
    # ou podemos simplesmente não usar este plot se ele não se encaixa.
    # Por enquanto, vamos criar um plot vazio ou um que não seja exatamente "price_plot".
    # A melhor abordagem aqui é criar um gráfico de payoff se o K for passado.
    # Como não temos K na função de plot, vamos criar um gráfico simples que seja um placeholder
    # ou focar apenas na distribuição.
    # Para o template, vamos criar um plot simples de exemplo para "price_plot"
    # que não representa caminhos de preço, mas pode ser um placeholder.
    plt.figure(figsize=(8, 6))
    plt.plot([0, len(ST_array)], [np.mean(ST_array), np.mean(ST_array)], 'r--')
    plt.text(len(ST_array)/2, np.mean(ST_array) * 1.05, f'Média de ST: {np.mean(ST_array):.2f}', horizontalalignment='center')
    plt.title('Média dos Preços do Ativo no Vencimento')
    plt.xlabel('Simulações')
    plt.ylabel('Preço do Ativo')
    plt.grid(True)
    buf_price = io.BytesIO()
    plt.savefig(buf_price, format='png')
    plt.close()
    data_price = base64.b64encode(buf_price.getvalue()).decode('utf-8')


    return data_price, data_dist