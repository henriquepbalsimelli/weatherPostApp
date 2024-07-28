# Instruções para executar a aplicação

1. É necessário o Docker instalado
2. Clone o projeto (git clone https://github.com/henriquepbalsimelli/weatherPostApp.git)
3. Insira o arquivo .env na pasta /app
4. Rode o seguinte comando: docker build -t weatherappimage .
5. Após o build, rode o seguinte comando: docker run -d --name weatherappcontainer -p 80:80 weatherappimage
6. Vá até http://127.0.0.1/docs para ter acesso à documentação.


Obs: caso você tente buildar a aplicação sem a .env, o sistema não irá funcionar. Para arrumar, terá que excluir a imagem e o container criados e builda-los de novo.

