import os
import mimetypes
import webapp2

class StaticHandler(webapp2.RequestHandler):
    ROOT_PATH = os.path.join(os.getcwd(), 'static')

    def get(self, filepath):
        filepath = os.path.join(self.ROOT_PATH, filepath)

        # Caso o caminho seja uma pasta exibir 403 Nao permitido
        if os.path.isdir(filepath):
            self.abort(403)

        # Caso nao encontre o arquivo exibir um 404 Nao encontrado
        if not os.path.exists(filepath):
            self.abort(404)

        # Envia o arquivo
        try:
            with open(filepath, 'r') as f:
                self.response.content_type = mimetypes.guess_type(filepath)[0]
                self.response.out.write(f.read())
        except:
            self.abort(404)
