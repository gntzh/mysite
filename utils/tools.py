def get_tree(node, fields):
    '''递归得到树形结构
    '''
    rst = {field: getattr(node, field, None) for field in fields}
    rst['children'] = []
    for child in node.get_children():
        rst['children'].append(get_tree(child, fields))
    return rst
