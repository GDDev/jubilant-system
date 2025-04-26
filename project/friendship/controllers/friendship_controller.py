from .. import friendship


@friendship.route('/adicionar', methods=['GET', 'POST'])
def add():
    pass

@friendship.route('/remover', methods=['GET', 'POST'])
def remove():
    pass

@friendship.route('/listar', methods=['GET'])
def get_all():
    pass