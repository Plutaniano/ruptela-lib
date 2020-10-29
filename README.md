# Ruptela-Lib

A Ruptela-Lib é uma biblioteca Python criada para facilitar a automação da interação com a plataforma "Locator Control Manager" da Ruptela, principalmente nas funções de criar objeto, criar SIM card e encontrar o número de telefone associado a um ICCID. Também possui scripts para a criação de gráficos.


# Instalação

Na aba "releases" do GitHub é possível baixar um arquivo .exe independente, que roda nativamente no Windows sem precisar de qualquer conhecimento de Python ou instalação.

Se quiser baixar e executar os arquivos Python diretamente, execute os seguinte comandos no Powershell do Windows:
```
git clone https://github.com/Plutaniano/ruptela
cd ruptela
python3 main.py
```
Para executar os comandos acima é necessário ter o Python, o git e as bibliotecas listadas no requirements.txt instaladas.


## Funções da Biblioteca

## Locator

### Objeto "Locator"
O objeto Locator é onde encontram-se os metodos e propriedades relacionadas ao Locator. A lista completa de propriedades e metodos pode ser encontrada no arquivo locator.py alguns exemplos abaixo:

```
>> from locator import Locator
>> l = Locator()
Login OK!
3 clientes criados.

>> l.session			# objeto requests.Session, guarda os cookies obtidos após login no site
<requests.sessions.Session object at 0x0000021423F1D1F0>

>> l.create_new_object(phone, client)		# cria um objeto na plataforma

>> l.create_sim(phone, cliente)			# cria sim card na plataforma
```

### Objeto "Client"
Objeto que guarda os metodos e propriedades de cada cliente. Podem ser acessados através do objeto Locator.
```
>> l.clients 					# lista de clientes existentes e seus IDs
[[51879] Colorado, [51071] EXCELbr, [52860] TESTE]

>> l.Colorado					# cada cliente é uma propriedade do objeto locator
[51879] Colorado

>> l.Colorado.objects				# lista com todos os objetos cadastrados no cliente
[[Obj][670364], [Obj][399907], [Obj][670323], [Obj][597336], [Obj][598326], ...]

>> l.Colorado.web_users 			# lista de web users do cliente
[[web id:785695] Fazenda Colorado, [web id:786026] Fazenda Colorado Adm]

>> l.Colorado.api_key				# api-key do primeiro webuser
'QQBP32xU4EoXlDGuNFTfce32HWYcwyHi'

>> l.Colorado.id				# id do cliente na plataforma
'51879'
```
### Objeto "Object"
Cada Object representa um dispositivo Ruptela cadastrado na plataforma, podem ser acessados através do objeto "Client".
```
>> l.Colorado.objects[0]			# Primeiro objeto da lista de objetos
[Obj][670364]

>> l.Colorado.objects[0].get_interval(7)	# retorna os pacotes de 7 dias atrás até agora
[[670364][2020-07-27T02:35:39] [gsm:2], [670364][2020-07-27T02:35:53] [gsm:2], ...]

>> l.Colorado.objects[0].get_interval(10, 7)	# retorna os pacotes entre 10 dias atrás e 7 dias atrás
[[670364][2020-07-27T02:35:39] [gsm:2], [670364][2020-07-27T02:35:53] [gsm:2], ...]
```

## Arqia

### Objeto "Arqia"
O objeto Arqia guarda os métodos e propriedades relacionados à Arqia.
```
>> from arqia import Arqia
>> a = Arqia()
Seja bem-vindo à Plataforma de Consumo da Arqia.

>> a.simcards					# lista de sim cards cadastrados na Arqia
[[SIM] +55 (62) 97601-3414, [SIM] +55 (14) 97601-0946, [SIM] +55 (14) 97601-0948, ...]

>> a.simcards[0].ICCID				# ICCID do primeiro sim card da lista  
'89551805500000007841'

>> a.simcards[0].phone				# número de telefone do simcards
'5519976134474'
```


# Erros
### Erros relacionados a chromedriver.exe

Provavelmente o chromedriver.exe está numa versão incompatível com a versão do Chrome instalada no computador. Verifique a versão do Chrome, baixe o chromedriver.exe correspondente e coloquei o na pasta do Cadastrador.


