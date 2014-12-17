===================================================================================================================================================================================

E89 - TOOLS

===================================================================================================================================================================================

O plugin E89 - TOOLS disponibiliza algumas ferramentas para o desenvolvimento django.

===================================================================================================================================================================================

Para utilizar o plugin, seguir os passos:

1) Instalar o plugin com pip.

2) No arquivo settings.py, adicionar "e89_tools" na lista de INSTALLED_APPS.

3) Inserir no arquivo settings.py as opções de configuração explicadas em sequência.

4) Rodar ./manage.py migrate para criar tabela de KeyValueStore.



Ferramentas disponíveis
-----------------------

	O plugin E89 - TOOLS disponibiliza as seguintes ferramentas:

		MODELS
		------
			KeyValueStore
				Model que possibilita o armazenamento de pares chave-valor. As instâncias desse model não devem ser criadas diretamente, mas sim acessadas através dos métodos estáticos set_value e get_int/get_list.

				Para armazenar um valor, basta utilizar o método estático KeyValueStore.set_value(key,value). Podem ser armazenados números inteiros assim como listas.
				Para recuperar um valor armazenado, basta utilizar o método estático KeyValueStore.get_int(key) ou KeyValueStore.get_list(key). Ambos esses métodos podem receber o parâmetro "default" que define um valor a ser retornado caso não seja encontrado um valor para o key fornecido. Por padrão o parâmetro "default" é None.

		FUNÇÕES - e89_tools.tools
		-------------------------

			print_console(msg)
				Função para imprimir uma mensagem no console. Faz checagem para impedir erros com caracteres unicode.

			deepgetattr(obj, attr)
				Função que busca um atributo de um objeto composto. Por exemplo, para um objeto "house" que possui um atributo chamado "address" e esse atributo por sua vez possui um atributo chamado "street", o valor do atributo "street" pode ser obtido através do chamado: street = deepgetattr(house,"addess__street")

			date_to_string(val, local=False, format="%Y-%m-%d %H:%M:%S.%f %Z"):
				Função que converte uma data (datetime) em uma string de acordo com o formato passado.  Caso o parâmetro "local" seja True, é utilizado o horário local.

			string_to_date(val)
				Função que converte uma string contendo uma data em um objeto datetime.

			send_email(user,subject,template,template_kwargs={},attachments=[],static_images=[],html=False)
				Função que envia um e-mail para o usuário passado como parâmetro.

				Parâmetros:
					user: poderá ser um objeto "auth.user" ou um objeto que possua um atributo "email", uma lista de objetos "auth.user", um QuerySet de objetos "auth.user" ou uma string contendo um e-mail.
					subject: string igual ao assunto do e-mail.
					template: string representando o template a ser utilizado para a mensagem de e-mail.
					template_kwargs: dicionário contendo parâmetros a serem passados ao template do e-mail
					attachments: lista de arquivos a serem anexados. A lista deve estar no formato [[nome_arquivo, arquivo],...]
					static_images: lista de strings contendo urls de arquivos estáticos a serem inseridos no e-mail.
					html: booleano indicando se o conteúdo do e-mail é html.

			concatenar_valores(objetos, sep=None)
				Concatena uma lista de strings separando-as por vírgula e incluindo um "e" antes do último item. Caso o parâmetro sep seja passado, esse separador é utilizado e o "e" não é colocado antes do último item.

        		Ex:
        			concatenar_valores(['pera',u'maçã','uva']) >>  'Pera, maçã e uva'
        			concatenar_valores(['pera',u'maçã','uva'],sep='|') >>  'Pera|maçã|uva'


        FERRAMENTAS PARA RELATÓRIOS - e89_tools.report_tools
        ----------------------------------------------------

        		UnicodeWriter
        			Classe utilizada junto com a biblioteca geraldo_reports para escrever arquivos CSV que contêm caracteres unicode.

			        Ex:
			            relatorio = accounts.reports.AlertasReport(request.user.usercrmv,ramos=ramos,delegacias=delegacias,data_filtro=data_filtro)
			            resp = HttpResponse(content_type='text/csv')

			            from geraldo.generators import CSVGenerator
			            import tools.report_tools
			            relatorio.generate_by(CSVGenerator, filename=resp,writer=tools.report_tools.UnicodeWriter(resp))


			    drop_shadow
			    	Função para inserir sombra em uma imagem inserida em um relatório.

		DECORATORS - e89_tools.decorators
		---------------------------------

			any_permission_required(*args)
				Decorator que permite que um usuário acesse uma view se ele possuir pelo menos uma das permissões passadas.

				Ex:
					@any_permission_required('auth.my_permission1','auth.my_permission2')
					def my_view(request):
						return HttpResponse('You're in!'')

			check_secret
				Decorator que só permite que uma view seja acessada caso o secret da aplicação django esteja sendo passado como um parâmetro do POST.


OPÇÕES NO ARQUIVO settings.py
===============================

Para funcionamento correto, as seguintes opções devem ser definidas no arquivo settings.py (valores mostrados como exemplo):

	EMAIL_HOST_ADDRESS
	------------------
	Endereço de e-mail utilizado para o envio de e-mails.


	EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
	--------------------------------------------------------------------------------
	Opções necessárias para envio de e-mail. Olhar https://docs.djangoproject.com/en/dev/ref/settings/#email-host

