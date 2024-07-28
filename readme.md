Para que as integrações funcionem como devem, você precisa criar uma conta no site https://openweathermap.org e obter as credenciais para poder realizar requisições à API deles. 
Assim que conseguir a chave de API, substitua o valor fornecido por eles e insira na variável WEATHER_APP_API_KEY.

Além disso, para que o sistema consiga realizar postagens em seu nome no X, você deve habilitar a conta de desenvolvedor: https://developer.x.com/en 
Nesse portal, você deve criar um projeto e obter as credenciais necessárias para realizar a integração.

```
  X_API_KEY -> é fornecedio apenas uma vez durante a criação do projeto no portal do desenvolvedor
  X_API_SECRET_KEY -> fornecido juntamente com X_API_KEY
  X_ACCESS_TOKEN -> Na aba "chaves e token" da sua aplicação no portal do desenvolvedor, você poderá gerar uma chave dessa.
  X_ACCESS_TOKEN_SECRET -> Será fornecedia juntamente com X_ACCESS_TOKEN.
```

# Instruções para executar a aplicação

1. É necessário o Docker instalado
2. Clone o projeto (git clone https://github.com/henriquepbalsimelli/weatherPostApp.git)
3. Insira o arquivo .env na pasta /app
4. Rode o seguinte comando: docker build -t weatherappimage .
5. Após o build, rode o seguinte comando: docker run -d --name weatherappcontainer -p 80:80 weatherappimage
6. Vá até http://127.0.0.1/docs para ter acesso à documentação.


Obs: caso você tente buildar a aplicação sem a .env, o sistema não irá funcionar. Para arrumar, terá que excluir a imagem e o container criados e builda-los de novo.
