import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from estocasticos.use_cases.financial_options.black_scholes_merton_use_case import BlackScholesMertonUseCase
from estocasticos.use_cases.financial_options.black_sholes_use_case import BlackScholesModelUseCase
from estocasticos.use_cases.financial_options.cox_ross_rubinstein_use_case import CoxRossRubinsteinUseCase

@login_required(login_url='/admin/login/')
def black_scholes_template(request):
    return render(request, "site/financeiros/black-sholes.html")

@login_required(login_url='/admin/login/')
def black_scholes_merton_template(request):
    return render(request, "site/financeiros/black-scholes-merton.html")

@login_required(login_url='/admin/login/')
def cox_ross_rubinstein_template(request):
    return render(request, "site/financeiros/cox-ross-rubinstein.html")

def black_scholes_view(request):
    print(request)
    if request.method == 'POST':
        try:
            S = float(request.POST.get('asset_price', 0))
            E = float(request.POST.get('exercise_price', 0))
            r = float(request.POST.get('interest_rate', 0))
            sigma = float(request.POST.get('volatility', 0))
            T = float(request.POST.get('time_to_expiration', 0))
            option_type = request.POST.get('option_type', 'call')
            # Validate inputs
            if S <= 0 or E <= 0 or T <= 0 or sigma <= 0:
                return JsonResponse({'error': 'All values must be positive.'})
            
            model = BlackScholesModelUseCase(S, E, r, sigma, T, option_type)
            d1, d2 = model.calculate_d1_d2()
            option_price = model.calculate_price()
            greeks = model.calculate_greeks()
            price_plot = model.plot_price_vs_underlying()
            payoff_plot = model.plot_payoff_at_expiration()
            break_even = 0
            # Interpretation text
            if option_type == 'call':
                break_even = round(E + option_price, 2)
                interpretation = f"""
                <h4>Interpretação dos Resultados:</h4>
                <p>O preço teórico da opção de compra é <strong>R$ {option_price}</strong>.</p>
                <p><strong>Delta de {greeks['delta']}</strong> significa que para cada R$ 1,00 de aumento no preço do ativo subjacente, 
                o preço da opção aumentará aproximadamente R$ {greeks['delta']}.</p>
                <p><strong>Gamma de {greeks['gamma']}</strong> indica quanto o delta mudará para cada R$ 1,00 de movimento no preço do ativo subjacente.</p>
                <p><strong>Theta de {greeks['theta']}</strong> mostra quanto valor a opção perde por dia apenas com a passagem do tempo.</p>
                <p><strong>Vega de {greeks['vega']}</strong> representa quanto o preço da opção mudará para cada 1% de alteração na volatilidade.</p>
                <p>Seu <strong>ponto de equilíbrio</strong> é quando o ativo subjacente atinge R$ {break_even} no vencimento.</p>
                <p>Seu <strong>risco máximo</strong> é o prêmio pago pela opção: R$ {option_price}.</p>
                <p>Seu <strong>ganho potencial é teoricamente ilimitado</strong> se o preço do ativo subjacente subir significativamente.</p>
                """
            else:
                break_even = round(E - option_price, 2)
                interpretation = f"""
                <h4>Interpretação dos Resultados:</h4>
                <p>O preço teórico da opção de venda é <strong>R$ {option_price}</strong>.</p>
                <p><strong>Delta de {greeks['delta']}</strong> significa que para cada R$ 1,00 de aumento no preço do ativo subjacente, 
                o preço da opção diminuirá aproximadamente R$ {abs(greeks['delta'])}.</p>
                <p><strong>Gamma de {greeks['gamma']}</strong> indica quanto o delta mudará para cada R$ 1,00 de movimento no preço do ativo subjacente.</p>
                <p><strong>Theta de {greeks['theta']}</strong> mostra quanto valor a opção perde por dia apenas com a passagem do tempo.</p>
                <p><strong>Vega de {greeks['vega']}</strong> representa quanto o preço da opção mudará para cada 1% de alteração na volatilidade.</p>
                <p>Seu <strong>ponto de equilíbrio</strong> é quando o ativo subjacente atinge R$ {break_even} no vencimento.</p>
                <p>Seu <strong>risco máximo</strong> é o prêmio pago pela opção: R$ {option_price}.</p>
                <p>Seu <strong>ganho potencial máximo</strong> é de R$ {break_even} se o preço do ativo subjacente cair para zero.</p>
                """
            
            return JsonResponse({
                'option_price': option_price,
                'greeks': greeks,
                'price_plot': price_plot,
                'payoff_plot': payoff_plot,
                'interpretation': interpretation,
                'd1': d1,
                'd2': d2,
                'break_even' :break_even,
                'max_loss' : option_price,
            })
            
        except ValueError as e:
            return JsonResponse({'error': 'Por favor, insira valores numéricos válidos.'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    return render(request, 'black_scholes.html')

def black_scholes_merton_view(request):
    """Handle API requests for Black-Scholes-Merton calculations."""
    if request.method == 'POST':
        try:
            # Extract parameters from POST data
            S = float(request.POST.get('asset_price', 0))
            E = float(request.POST.get('exercise_price', 0))
            r = float(request.POST.get('interest_rate', 0))
            sigma = float(request.POST.get('volatility', 0))
            T = float(request.POST.get('time_to_expiration', 0))
            option_type = request.POST.get('option_type', 'call')
            dividend_yield = float(request.POST.get('dividend_yield', 0))
            
            # Validate input
            if S <= 0 or E <= 0 or T <= 0 or sigma <= 0:
                return JsonResponse({'error': 'All values must be positive.'})
            
            # Create model and perform calculations
            model = BlackScholesMertonUseCase(S, E, r, sigma, T, option_type, dividend_yield)
            d1, d2 = model.calculate_d1_d2()
            option_price = model.calculate_price()
            greeks = model.calculate_greeks()
            price_plot = model.plot_price_vs_underlying()
            payoff_plot = model.plot_payoff_at_expiration()
            
            # Calculate break-even point
            if option_type == 'call':
                break_even = round(E + option_price, 2)
                interpretation = f"""
                <h4>Interpretação dos Resultados:</h4>
                <p>O preço teórico da opção de compra é <strong>R$ {option_price}</strong>.</p>
                <p><strong>Delta de {greeks['delta']}</strong> significa que para cada R$ 1,00 de aumento no preço do ativo subjacente, 
                o preço da opção aumentará aproximadamente R$ {greeks['delta']}.</p>
                <p><strong>Gamma de {greeks['gamma']}</strong> indica quanto o delta mudará para cada R$ 1,00 de movimento no preço do ativo subjacente.</p>
                <p><strong>Theta de {greeks['theta']}</strong> mostra quanto valor a opção perde por dia apenas com a passagem do tempo.</p>
                <p><strong>Vega de {greeks['vega']}</strong> representa quanto o preço da opção mudará para cada 1% de alteração na volatilidade.</p>
                <p><strong>Rho de {greeks['rho']}</strong> indica a sensibilidade do preço da opção em relação a mudanças na taxa de juros livre de risco.</p>
                <p>O rendimento de dividendos de <strong>{dividend_yield}%</strong> reduz o valor da opção de compra em comparação com um ativo sem dividendos.</p>
                <p>Seu <strong>ponto de equilíbrio</strong> é quando o ativo subjacente atinge R$ {break_even} no vencimento.</p>
                <p>Seu <strong>risco máximo</strong> é o prêmio pago pela opção: R$ {option_price}.</p>
                <p>Seu <strong>ganho potencial é teoricamente ilimitado</strong> se o preço do ativo subjacente subir significativamente.</p>
                """
            else:
                break_even = round(E - option_price, 2)
                interpretation = f"""
                <h4>Interpretação dos Resultados:</h4>
                <p>O preço teórico da opção de venda é <strong>R$ {option_price}</strong>.</p>
                <p><strong>Delta de {greeks['delta']}</strong> significa que para cada R$ 1,00 de aumento no preço do ativo subjacente, 
                o preço da opção diminuirá aproximadamente R$ {abs(greeks['delta'])}.</p>
                <p><strong>Gamma de {greeks['gamma']}</strong> indica quanto o delta mudará para cada R$ 1,00 de movimento no preço do ativo subjacente.</p>
                <p><strong>Theta de {greeks['theta']}</strong> mostra quanto valor a opção perde por dia apenas com a passagem do tempo.</p>
                <p><strong>Vega de {greeks['vega']}</strong> representa quanto o preço da opção mudará para cada 1% de alteração na volatilidade.</p>
                <p><strong>Rho de {greeks['rho']}</strong> indica a sensibilidade do preço da opção em relação a mudanças na taxa de juros livre de risco.</p>
                <p>O rendimento de dividendos de <strong>{dividend_yield}%</strong> aumenta o valor da opção de venda em comparação com um ativo sem dividendos.</p>
                <p>Seu <strong>ponto de equilíbrio</strong> é quando o ativo subjacente atinge R$ {break_even} no vencimento.</p>
                <p>Seu <strong>risco máximo</strong> é o prêmio pago pela opção: R$ {option_price}.</p>
                <p>Seu <strong>ganho potencial máximo</strong> é de R$ {break_even} se o preço do ativo subjacente cair para zero.</p>
                """
            
            # Return JSON response with calculations
            return JsonResponse({
                'option_price': option_price,
                'greeks': greeks,
                'price_plot': price_plot,
                'payoff_plot': payoff_plot,
                'interpretation': interpretation,
                'd1': d1,
                'd2': d2,
                'break_even': break_even,
                'max_loss': option_price,
            })
            
        except ValueError:
            return JsonResponse({'error': 'Por favor, insira valores numéricos válidos.'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    # If not POST, just render the template
    return render(request, 'site/financeiros/black-scholes-merton.html')

def cox_ross_rubinstein_view(request):
    """Handle API requests for Cox-Ross-Rubinstein calculations."""
    if request.method == 'POST':
        try:
            # Extract parameters from POST data
            S = float(request.POST.get('asset_price', 0))
            E = float(request.POST.get('exercise_price', 0))
            r = float(request.POST.get('interest_rate', 0))
            sigma = float(request.POST.get('volatility', 0))
            T = float(request.POST.get('time_to_expiration', 0))
            option_type = request.POST.get('option_type', 'call')
            steps = int(request.POST.get('steps', 5))
            dividend_yield = float(request.POST.get('dividend_yield', 0))
            
            # Validate input
            if S <= 0 or E <= 0 or T <= 0 or sigma <= 0 or steps <= 0:
                return JsonResponse({'error': 'All values must be positive. Steps must be a positive integer.'})
            
            # Limit steps to a reasonable number for visualization
            if steps > 10:
                steps = 10
            
            # Create model and perform calculations
            model = CoxRossRubinsteinUseCase(S, E, r, sigma, T, option_type, steps, dividend_yield)
            option_price = model.calculate_price()
            greeks = model.calculate_greeks()
            
            # Get lattice data and generate HTML
            lattice_html = model.generate_lattice_html()
            lattice_data = model.get_lattice_data()
            
            # Calculate traditional NPV (simplified assumption: NPV = S - E)
            traditional_npv = S - E
            
            # Calculate expanded NPV (traditional NPV + option value)
            expanded_npv = traditional_npv + option_price if traditional_npv < 0 else traditional_npv
            
            # Value of flexibility (equals option value for negative NPV projects)
            flexibility_value = option_price if traditional_npv < 0 else 0
            
            # Option value / investment cost ratio
            option_ratio = option_price / E
            
            # Calculate break-even point
            if option_type == 'call':
                break_even = round(E + option_price, 2)
                interpretation = f"""
                <h4>Interpretação dos Resultados:</h4>
                <p>O preço da opção de compra calculado pelo modelo binomial de Cox-Ross-Rubinstein é <strong>R$ {option_price}</strong>.</p>
                <p>O modelo usa <strong>{steps} passos</strong> para construir uma árvore binomial, com fator de alta (u) de {lattice_data['u']} e fator de baixa (d) de {lattice_data['d']}.</p>
                <p><strong>Delta de {greeks['delta']}</strong> significa que para cada R$ 1,00 de aumento no preço do ativo subjacente, 
                o preço da opção aumentará aproximadamente R$ {greeks['delta']}.</p>
                <p><strong>Gamma de {greeks['gamma']}</strong> indica quanto o delta mudará para cada R$ 1,00 de movimento no preço do ativo subjacente.</p>
                <p><strong>Theta de {greeks['theta']}</strong> mostra quanto valor a opção perde por dia apenas com a passagem do tempo.</p>
                <p><strong>Vega de {greeks['vega']}</strong> representa quanto o preço da opção mudará para cada 1% de alteração na volatilidade.</p>
                <p><strong>Rho de {greeks['rho']}</strong> indica a sensibilidade do preço da opção em relação a mudanças na taxa de juros livre de risco.</p>
                <p>O rendimento de dividendos de <strong>{dividend_yield}%</strong> reduz o valor da opção de compra em comparação com um ativo sem dividendos.</p>
                <p>Seu <strong>ponto de equilíbrio</strong> é quando o ativo subjacente atinge R$ {break_even} no vencimento.</p>
                <p>Seu <strong>risco máximo</strong> é o prêmio pago pela opção: R$ {option_price}.</p>
                <p>Seu <strong>ganho potencial é teoricamente ilimitado</strong> se o preço do ativo subjacente subir significativamente.</p>
                <p>A probabilidade neutra ao risco (p) usada no modelo é de <strong>{lattice_data['p'] * 100:.2f}%</strong>.</p>
                
                <h5>Análise de Opções Reais:</h5>
                <p>Se este fosse um projeto de investimento real:</p>
                <ul>
                    <li>O VPL tradicional seria <strong>R$ {traditional_npv:.2f}</strong></li>
                    <li>O VPL expandido (com flexibilidade) seria <strong>R$ {expanded_npv:.2f}</strong></li>
                    <li>O valor da flexibilidade seria <strong>R$ {flexibility_value:.2f}</strong></li>
                    <li>A razão valor da opção / custo de investimento seria <strong>{option_ratio:.4f}</strong></li>
                </ul>
                
                <h5>Interpretação da Treliça Binomial:</h5>
                <p>Na visualização da treliça binomial:</p>
                <ul>
                    <li><strong>Preço da Ação</strong>: Valor do ativo subjacente em cada nó</li>
                    <li><strong>Valor da Opção</strong>: Valor da opção em cada nó</li>
                    <li><strong>Valor Intrínseco</strong>: Valor de exercício imediato (max(0, S-K) para calls)</li>
                </ul>
                <p>As células verdes representam situações onde a opção está "in-the-money" (preço do ativo > preço de exercício para calls).</p>
                """
            else:  # put option
                break_even = round(E - option_price, 2)
                interpretation = f"""
                <h4>Interpretação dos Resultados:</h4>
                <p>O preço da opção de venda calculado pelo modelo binomial de Cox-Ross-Rubinstein é <strong>R$ {option_price}</strong>.</p>
                <p>O modelo usa <strong>{steps} passos</strong> para construir uma árvore binomial, com fator de alta (u) de {lattice_data['u']} e fator de baixa (d) de {lattice_data['d']}.</p>
                <p><strong>Delta de {greeks['delta']}</strong> significa que para cada R$ 1,00 de aumento no preço do ativo subjacente, 
                o preço da opção diminuirá aproximadamente R$ {abs(greeks['delta'])}.</p>
                <p><strong>Gamma de {greeks['gamma']}</strong> indica quanto o delta mudará para cada R$ 1,00 de movimento no preço do ativo subjacente.</p>
                <p><strong>Theta de {greeks['theta']}</strong> mostra quanto valor a opção perde por dia apenas com a passagem do tempo.</p>
                <p><strong>Vega de {greeks['vega']}</strong> representa quanto o preço da opção mudará para cada 1% de alteração na volatilidade.</p>
                <p><strong>Rho de {greeks['rho']}</strong> indica a sensibilidade do preço da opção em relação a mudanças na taxa de juros livre de risco.</p>
                <p>O rendimento de dividendos de <strong>{dividend_yield}%</strong> aumenta o valor da opção de venda em comparação com um ativo sem dividendos.</p>
                <p>Seu <strong>ponto de equilíbrio</strong> é quando o ativo subjacente atinge R$ {break_even} no vencimento.</p>
                <p>Seu <strong>risco máximo</strong> é o prêmio pago pela opção: R$ {option_price}.</p>
                <p>Seu <strong>ganho potencial máximo</strong> é de R$ {break_even} se o preço do ativo subjacente cair para zero.</p>
                <p>A probabilidade neutra ao risco (p) usada no modelo é de <strong>{lattice_data['p'] * 100:.2f}%</strong>.</p>
                
                <h5>Análise de Opções Reais:</h5>
                <p>Se este fosse um projeto de investimento real (opção de abandono):</p>
                <ul>
                    <li>O VPL tradicional seria <strong>R$ {traditional_npv:.2f}</strong></li>
                    <li>O VPL expandido (com flexibilidade) seria <strong>R$ {expanded_npv:.2f}</strong></li>
                    <li>O valor da flexibilidade seria <strong>R$ {flexibility_value:.2f}</strong></li>
                    <li>A razão valor da opção / custo de investimento seria <strong>{option_ratio:.4f}</strong></li>
                </ul>
                
                <h5>Interpretação da Treliça Binomial:</h5>
                <p>Na visualização da treliça binomial:</p>
                <ul>
                    <li><strong>Preço da Ação</strong>: Valor do ativo subjacente em cada nó</li>
                    <li><strong>Valor da Opção</strong>: Valor da opção em cada nó</li>
                    <li><strong>Valor Intrínseco</strong>: Valor de exercício imediato (max(0, K-S) para puts)</li>
                </ul>
                <p>As células verdes representam situações onde a opção está "in-the-money" (preço do ativo < preço de exercício para puts).</p>
                """
            
            # Return JSON response with calculations
            response_data = {
                'option_price': option_price,
                'greeks': greeks,
                'lattice_html': lattice_html,
                'interpretation': interpretation,
                'break_even': break_even,
                'max_loss': option_price,
                'u': lattice_data['u'],
                'd': lattice_data['d'],
                'p': lattice_data['p'],
                'dt': lattice_data['dt'],
                'traditional_npv': traditional_npv,
                'expanded_npv': expanded_npv,
                'flexibility_value': flexibility_value,
                'option_ratio': option_ratio
            }
            
            return JsonResponse(response_data)
            
        except ValueError:
            return JsonResponse({'error': 'Por favor, insira valores numéricos válidos. O número de passos deve ser um número inteiro.'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    # If not POST, just render the template
    return render(request, 'site/financeiros/cox-ross-rubinstein.html')
