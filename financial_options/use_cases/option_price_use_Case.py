# core/precificacao_opcoes_monte_carlo.py
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def option_price_use_case(S0, K, T, r, sigma, num_simulacoes, option_type='call'):
    """
    Simula o preço de opções europeias usando o método de Monte Carlo.

    Args:
        S0 (float): Preço atual do ativo subjacente.
        K (float): Preço de exercício (strike) da opção.
        T (float): Tempo até o vencimento em anos.
        r (float): Taxa de juros livre de risco anual (em %).
        sigma (float): Volatilidade anual do ativo subjacente (em %).
        num_simulacoes (int): Número de simulações de Monte Carlo.
        option_type (str): Tipo da opção, 'call' ou 'put'.

    Returns:
        tuple: (preco_opcao, ST_array, statistics)
            preco_opcao (float): Preço estimado da opção europeia.
            ST_array (numpy.ndarray): Array dos preços simulados do ativo no vencimento.
            statistics (dict): Dicionário com estatísticas descritivas dos preços no vencimento.
    """
    # Converter taxas de porcentagem para decimal
    r_dec = r / 100.0
    sigma_dec = sigma / 100.0
    
    # Gerar números aleatórios da distribuição normal padrão
    z = np.random.standard_normal(num_simulacoes)
    
    # Simular os preços do ativo subjacente no vencimento (ST)
    ST = S0 * np.exp((r_dec - 0.5 * sigma_dec**2) * T + sigma_dec * np.sqrt(T) * z)

    # Calcular o payoff da opção com base no tipo
    if option_type == 'call':
        payoffs = np.maximum(ST - K, 0)
    elif option_type == 'put':
        payoffs = np.maximum(K - ST, 0)
    else:
        # Caso o tipo seja inválido, retorna um erro. A validação principal está na view.
        raise ValueError("Tipo de opção inválido. Escolha 'call' ou 'put'.")

    # Calcular o preço da opção como a média dos payoffs descontados
    preco_opcao = np.exp(-r_dec * T) * np.mean(payoffs)

    # Calcular estatísticas descritivas dos preços finais simulados
    statistics = {
        'Média': np.mean(ST),
        'Mediana': np.median(ST),
        'Desvio Padrão': np.std(ST),
        'Mínimo': np.min(ST),
        'Máximo': np.max(ST),
    }

    return preco_opcao, ST, statistics

def create_plots(ST_array):
    """
    Cria gráficos para visualização dos resultados da simulação.
    """
    plt.style.use('seaborn-v0_8-darkgrid')

    # --- Gráfico 1: Convergência da Média do Preço ---
    mean_prices = np.cumsum(ST_array) / (np.arange(len(ST_array)) + 1)
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(mean_prices)
    ax1.set_title('Convergência do Preço Médio do Ativo')
    ax1.set_xlabel('Número de Simulações')
    ax1.set_ylabel('Preço Médio')
    ax1.grid(True)
    
    buf_price = io.BytesIO()
    fig1.savefig(buf_price, format='png', bbox_inches='tight')
    data_price = base64.b64encode(buf_price.getvalue()).decode('utf-8')
    plt.close(fig1)

    # --- Gráfico 2: Distribuição dos Preços Finais ---
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.hist(ST_array, bins=50, density=True, alpha=0.75, color='skyblue', edgecolor='black')
    ax2.set_title('Distribuição dos Preços do Ativo no Vencimento (ST)')
    ax2.set_xlabel('Preço do Ativo no Vencimento')
    ax2.set_ylabel('Densidade')
    ax2.grid(True)

    buf_dist = io.BytesIO()
    fig2.savefig(buf_dist, format='png', bbox_inches='tight')
    data_dist = base64.b64encode(buf_dist.getvalue()).decode('utf-8')
    plt.close(fig2)

    return data_price, data_dist